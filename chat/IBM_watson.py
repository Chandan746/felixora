import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='gRWFjDNlBUzpm-p9AknzexWMklizrvr7lRZ0343PYxDS',
    url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api'
)

response = natural_language_understanding.analyze(
    text="i am happy",
    features=Features(emotion=EmotionOptions())).get_result()

# print(json.dumps(response, indent=2))
emo_joy = (response['emotion']['document']['emotion']['joy'])
emo_anger = (response['emotion']['document']['emotion']['anger'])
emo_fear = (response['emotion']['document']['emotion']['fear'])
emo_sadness = (response['emotion']['document']['emotion']['sadness'])
emo_disgust = (response['emotion']['document']['emotion']['disgust'])
msg_emotion = ''
if (emo_joy) > (emo_anger and emo_fear and emo_sadness and emo_disgust):
    msg_emotion = 'emo_joy'
elif emo_anger > (emo_joy and emo_fear and emo_sadness and emo_disgust):
    msg_emotion = "emo_anger"
elif emo_fear > (emo_anger and emo_joy and emo_sadness and emo_disgust):
    msg_emotion = "emo_fear"
elif emo_sadness > (emo_anger and emo_fear and emo_joy and emo_disgust):
    msg_emotion = "emo_sadness"
elif emo_disgust > (emo_anger and emo_fear and emo_sadness and emo_joy):
    msg_emotion = "emo_disgust"
else: pass
print(msg_emotion)