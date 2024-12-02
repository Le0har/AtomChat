from django.core.management import BaseCommand, CommandError
from chat.models import Room, Message
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = 'Creating data for a database'

    def handle(self, *args, **options):
        # Creating users
        try:
            maksim, created = User.objects.get_or_create(username='maksim')
            if created:
                maksim.set_password('user_maks91')
                maksim.save()
            diana, created = User.objects.get_or_create(username='diana')
            if created:
                diana.set_password('user_dian92')
                diana.save()
            rodion, created = User.objects.get_or_create(username='rodion_admin', is_staff=True)
            if created:
                rodion.set_password('moder_rod93')
                rodion.save()
        except:
            raise CommandError('Can\'t create user!')

        # Creating private room for two users
        try:
                room_private, created = Room.objects.get_or_create(is_private=True, name=f'{maksim}&{diana}_private')
                if created:
                    room_private.users.set((maksim, diana))
        except:
                raise CommandError('Can\'t create private room for two users!')

        # Creating private room for several users
        try:
                room_common, created = Room.objects.get_or_create(is_private=True, name='Чат про погоду')
                if created:
                    room_common.users.set((maksim, diana, rodion))
        except:
                raise CommandError('Can\'t create private room for several users!')

        # Creating message in private room for two users
        try:
            Message.objects.create(text='Привет, как дела?', author=maksim, room=room_private)
        except:
            raise CommandError('Can\'t create message in room!')
        
        self.stdout.write(self.style.SUCCESS('Database entries have been created successfully!'))
