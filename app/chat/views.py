from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from chat.models import Message, Room
from chat.serializers import MessageOneToOneSerializer, RoomSerializer, MessageSerializer
from chat.serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.permissions import IsRoomUser


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all() 
    serializer_class = MessageOneToOneSerializer 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all() 
    serializer_class = RoomSerializer 
    permission_classes = (IsAuthenticated, IsRoomUser)
    lookup_url_kwarg = 'room_id'


class RoomMessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer 
    permission_classes = (IsAuthenticated, IsRoomUser) 

    def _get_room(self):
        room_id = self.kwargs['room_id']
        return get_object_or_404(Room, pk=room_id)

    def get_queryset(self):
        room = self._get_room()
        return room.messages
    
    def perform_create(self, serializer):
        room = self._get_room()
        serializer.save(room=room, author=self.request.user)


class UserCreateSet(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny, )


