from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    portfolio_site = models.URLField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    about = models.CharField(max_length=124, default='Hey there i am using felixora',null = False,blank=False)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    author = models.ForeignKey(
        User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chatbtwn = models.TextField()

    def __str__(self):
        return self.author.username

    def last_10_messages(roomname):
        return Message.objects.filter(chatbtwn = roomname).order_by('timestamp').all()
