from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from chat.models import Message, Room
from chat.serializers import MessageOneToOneSerializer, RoomSerializer, MessageSerializer
from chat.serializers import UserCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from chat.permissions import IsRoomUser, IsAdmin


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all() 
    serializer_class = MessageOneToOneSerializer 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all() 
    serializer_class = RoomSerializer 
    lookup_url_kwarg = 'room_id'

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.detail:
            permission_classes.append(IsRoomUser)
            # if self.request.method in ['PUT', 'GET']:
            #     permission_classes = [(IsAuthenticated & IsRoomUser) | (IsAuthenticated & IsAdmin)]
            # elif self.request.method == 'DELETE':
            #     permission_classes = [IsAuthenticated & IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        room_id = self.kwargs.get('room_id', None)
        if room_id is not None:
            return Room.objects.filter(pk=room_id)
        # current_user = self.request.user
        # if current_user.is_staff:
        #     return Room.objects.filter(is_private=True)
        # return Room.objects.filter(users=current_user)


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
    permission_classes = (AllowAny,)


