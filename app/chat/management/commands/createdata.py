from typing import Any
from django.core.management import BaseCommand, CommandError
from chat.models import User, Room, Message


class Command(BaseCommand):
    help = 'Creating data for a database'

    def handle(self, *args, **options):
        # Creating users
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
            try:
                User.objects.create(**user)
            except:
                raise CommandError('Can\'t create user!')

        # Creating private room for two users
        maksim = User.objects.get(username='maksim')
        diana = User.objects.get(username='diana')
        try:
                room_private = Room.objects.create(is_private=True, name=f'{maksim}&{diana}_private')
                room_private.users.set((maksim, diana))
        except:
                raise CommandError('Can\'t create private room for two users!')

        # Creating private room for several users
        rodion = User.objects.get(username='rodion_admin')
        try:
                room_common = Room.objects.create(is_private=True, name='Чат про погоду')
                room_common.users.set((maksim, diana, rodion))
        except:
                raise CommandError('Can\'t create private room for several users!')

        # Creating message in private room for two users
        try:
            Message.objects.create(text='Привет, как дела?', author=maksim, room=room_private)
        except:
            raise CommandError('Can\'t create message in room!')
        
        self.stdout.write(self.style.SUCCESS('Database entries have been created successfully!'))
