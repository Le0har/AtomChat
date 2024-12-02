from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from chat.models import Message, Room
from chat.serializers import MessageOneToOneSerializer, RoomSerializer, MessageSerializer
from chat.serializers import UserCreateSerializer, UserBlockSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from chat.permissions import IsRoomUser


User = get_user_model()


class MessageViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
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
            if self.request.method in ['PUT', 'GET']:
                permission_classes.append(IsRoomUser | IsAdminUser)
            elif self.request.method == 'DELETE':
                permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_staff:
            return Room.objects.all()
        return Room.objects.filter(users=current_user)


class RoomMessageViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = MessageSerializer 
    permission_classes = [IsAuthenticated, IsRoomUser | IsAdminUser]

    def _get_room(self):
        room_id = self.kwargs['room_id']
        return get_object_or_404(Room, pk=room_id)

    def get_queryset(self):
        room = self._get_room()
        return room.messages
    
    def perform_create(self, serializer):
        room = self._get_room()
        serializer.save(room=room, author=self.request.user)


class UserViewSet(mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    @action(detail=True, methods=['put'], permission_classes=[IsAdminUser])
    def block(self, request, pk):
        instance = self.get_object()
        serializer = UserBlockSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


