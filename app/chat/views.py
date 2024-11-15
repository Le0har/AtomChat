from django.shortcuts import render
from rest_framework import viewsets
from chat.models import Message
from chat.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer