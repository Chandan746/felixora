from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions



User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        try:
            messages = Message.last_10_messages(data['roomname'])
        except:
            messages =[]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
        
    def typing(self, data):
        return print("Yes its typing")

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.filter(username=author)[0]
        message = Message.objects.create(
            author=author_user,
            content=data['message'],
            chatbtwn=data['roomId'])
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'chatbtwn':message.chatbtwn
        }

 

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def smiley(self,event):
        message = event['message']
        
        natural_language_understanding = NaturalLanguageUnderstandingV1(
            version='2018-11-16',
            iam_apikey='gRWFjDNlBUzpm-p9AknzexWMklizrvr7lRZ0343PYxDS',
            url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
        )
        
        if len(message)>14:
            response = natural_language_understanding.analyze(
                text=str(message),
                features=Features(emotion=EmotionOptions())).get_result()

            print(json.dumps(response, indent=2))
            emo_joy = (response['emotion']['document']['emotion']['joy'])
            emo_anger = (response['emotion']['document']['emotion']['anger'])
            emo_fear = (response['emotion']['document']['emotion']['fear'])
            emo_sadness = (response['emotion']['document']['emotion']['sadness'])
            emo_disgust = (response['emotion']['document']['emotion']['disgust'])
            msg_emotion = ''
            if (emo_joy) > (emo_anger and emo_sadness ):
                msg_emotion = 'emo_joy'
                message = message +' :-)'
            elif emo_anger > (emo_joy  and emo_sadness ):
                msg_emotion = "emo_anger"
                message = message +' >:@'
        
            elif emo_sadness > (emo_anger and emo_joy):
                msg_emotion = "emo_sadness"
                message = message +' :-('
        else:
            pass
        print(message,"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        content = {
            'message':message,
            'from': event['from'],
            'roomId':event['roomId']
        }
        print(content)
        self.new_message(content)
        
        
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'typing': typing,
        'smiley':smiley,
    }