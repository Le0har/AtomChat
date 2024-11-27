from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Room(models.Model):
    name = models.CharField(unique=True)
    # Flag for private chats (for two) and private chats (for several)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(to=User, related_name='rooms')

    def __str__(self):
        return self.name
    

class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='messages')

    def __str__(self):
        return self.text