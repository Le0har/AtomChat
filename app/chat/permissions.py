from django.shortcuts import get_object_or_404
from rest_framework import permissions
from chat.models import Room


class IsRoomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        room_id = view.kwargs.get('room_id')
        room = get_object_or_404(Room, pk=room_id)
        return request.user in room.users.all()