from typing import Any
from django.core.management import BaseCommand
from chat.serializers import UserCreateSerializer, MessageOneToOneSerializer, RoomSerializer


class Command(BaseCommand):
    help = 'Creating data for a database'

    def handle(self, *args, **options):
        users = [
            {
                'username': 'maksim',
                'password': 'user_maks91'
            },
            {
                'username': 'diana',
                'password': 'user_dian92'
            },
            {
                'username': 'rodion_admin',
                'password': 'moder_rod93',
                'is_staff': True
            }
        ]
        for user in users:
            serializer = UserCreateSerializer(data=user)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        message_one_to_one = {
            'text': 'Привет, как дела?',
            'user_to': 38
        }
        serializer = MessageOneToOneSerializer(data=message_one_to_one)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        common_room = {
            "name": "Чат о погоде",
            "users": [38, 39, 40]
        }
        serializer = RoomSerializer(data=common_room)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.stdout.write(self.style.SUCCESS('Database entries have been created successfully!'))
