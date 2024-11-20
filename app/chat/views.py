from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from chat.models import Message, Room
from chat.serializers import MessageOneToOneSerializer, RoomSerializer, MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all() 
    serializer_class = MessageOneToOneSerializer 


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all() 
    serializer_class = RoomSerializer 


class RoomMessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer  

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        room = get_object_or_404(Room, pk=room_id)
        queryset = room.messages
        return queryset





