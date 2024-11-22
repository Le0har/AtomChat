from django.contrib.auth import get_user_model
from rest_framework import serializers
from chat.models import Message, Room


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Message
        fields = ('text', 'created_at', 'author') 
        read_only_fields = ['created_at']


class MessageOneToOneSerializer(MessageSerializer): 
    user_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta(MessageSerializer.Meta):
        fields = ('text', 'created_at', 'user_to') 
 
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
        fields = ('id', 'name', 'is_private', 'created_at')
        read_only_fields = ['is_private', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if 'users' in request._data:
            validated_data['users'] = (request._data['users'], ) + (request._user, )
        else:
            validated_data['users'] = (request._user, )
        return super().create(validated_data)    