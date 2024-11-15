from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Room(models.Model):
    name = models.CharField(unique=True)
    # Flag for private chats (for two) and private chats (?)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(to=User, related_name='rooms')

    def __str__(self):
        return self.name
    

class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE, related_name='room')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return self.text