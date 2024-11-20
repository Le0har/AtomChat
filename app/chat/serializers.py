from rest_framework import serializers
from chat.models import Message, Room
from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Message
        fields = ('text', 'created_at', 'room', 'author') 
        read_only_fields = ['created_at', 'room']


class MessageOneToOneSerializer(MessageSerializer): 
    user_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta(MessageSerializer.Meta):
        fields = ('text', 'created_at', 'author', 'user_to') 
 
    def create(self, validated_data):
        user_to = validated_data.pop('user_to')
        author = validated_data.get('author')
        room = Room.objects.filter(users=(author.pk, user_to.pk), is_private=True).first()
        if room is None:
            room = Room.objects.create(is_private=True, name=f'{author}&{user_to}_private')
            room.users.set((author, user_to))
        validated_data['room'] = room
        return super().create(validated_data)
    

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name', 'is_private', 'created_at', 'users')
        read_only_fields = ['created_at', 'is_private']