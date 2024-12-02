from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from chat.models import Message, Room


User = get_user_model()


def create_user(username, **kwds):
    user = User.objects.create(username=username, **kwds)
    passw = kwds.get('password')
    if passw:
        user.set_password(passw)
        user.save()
    return user

def create_room(name, users):
    room = Room.objects.create(name=name)
    room.users.set(users)
    return room


class RegisterTestCase(APITestCase):

    def test_ok_create_user(self):
        USERNAME = 'michael'
        number_records = User.objects.count()
        res = self.client.post(reverse('users-list'), {'username': USERNAME, 'password': 'user_mic1987'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), number_records + 1)
        new_user = User.objects.get(username=USERNAME)
        self.assertEqual(new_user.username, USERNAME)
        self.assertEqual(new_user.is_active, True)


class LoginTestCase(APITestCase): 

    def setUp(self):
        self.password = 'user_tam1971'
        self.user = create_user('tamara', password=self.password)

    def test_ok_create_token(self):
        res = self.client.post(reverse('get-token'), {'username': self.user.username, 'password': self.password})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_token = res.data['token']
        user_by_token = Token.objects.get(key=new_token).user
        self.assertEqual(user_by_token, self.user)


class MessageTestCase(APITestCase):

    def setUp(self):
        self.ruslan = create_user('ruslan')
        self.ludmila = create_user('ludmila')
        self.client.force_authenticate(user=self.ruslan)

    def test_ok_send_message(self):
        TEXTMESSAGE = 'Привет, как дела?'
        number_messages = Message.objects.count()
        number_rooms = Room.objects.count()
        res = self.client.post(reverse('message-list'), {'text': TEXTMESSAGE, 'user_to': self.ludmila.pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), number_messages + 1)
        new_message = Message.objects.get(text=TEXTMESSAGE)
        self.assertEqual(new_message.text, TEXTMESSAGE)
        self.assertEqual(new_message.author, self.ruslan)
        self.assertEqual(Room.objects.count(), number_rooms + 1)
        new_room = Room.objects.get(name=f'{self.ruslan}&{self.ludmila}_private')
        self.assertEqual(new_room.name, 'ruslan&ludmila_private')
        self.assertEqual(new_room.is_private, True)
        users_in_room = new_room.users.all()
        self.assertEqual(users_in_room.count(), 2)
        self.assertEqual([*users_in_room], [self.ruslan, self.ludmila])
        self.assertEqual(new_room.messages.count(), 1)
        self.assertIn(new_message, new_room.messages.all())


class RoomTestCase(APITestCase):

    def setUp(self):
        self.stepan = create_user('stepan')
        self.fedor = create_user('fedor')
        self.masha = create_user('masha') 
        self.client.force_authenticate(user=self.stepan)  

    def test_ok_create_room(self):
        ROOMNAME = 'Новости спорта'
        number_rooms = Room.objects.count()
        users_pk = [self.stepan.pk, self.fedor.pk, self.masha.pk]
        res = self.client.post(reverse('room-list'), {'name': ROOMNAME, 'users': users_pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Room.objects.count(), number_rooms + 1)
        new_room = Room.objects.get(name=ROOMNAME)
        self.assertEqual(new_room.name, ROOMNAME)
        self.assertEqual(new_room.is_private, True)
        users_in_room = new_room.users.all()
        self.assertEqual(users_in_room.count(), 3)
        self.assertEqual([*users_in_room], [self.stepan, self.fedor, self.masha])


class ListRoomTestCase(APITestCase):

    def setUp(self):
        self.ivan = create_user('ivan')
        self.fedor = create_user('fedor')
        self.masha = create_user('masha') 
        self.client.force_authenticate(user=self.ivan)
        self.room_first = create_room('Стихи Пушкина', [self.ivan, self.fedor])
        self.room_second = create_room('Новости кино', [self.ivan, self.masha])
        self.room_third = create_room('Заметки наблюдателя', [self.masha, self.fedor])

    def test_ok_get_list_rooms(self):
        res = self.client.get(reverse('room-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        number_rooms_in_db = Room.objects.count()
        number_rooms_in_response = len(res.data)
        self.assertNotEqual(number_rooms_in_db, number_rooms_in_response)
        self.assertEqual(number_rooms_in_response, 2)
        for room in res.data:
            self.assertEqual(self.ivan.pk in room['users'], True)


class UpdateRoomTestCase(APITestCase):

    def setUp(self):
        self.roman = create_user('roman')
        self.fedor = create_user('fedor')
        self.masha = create_user('masha')
        self.client.force_authenticate(user=self.roman)
        self.room = create_room('Фантазеры', [self.roman, self.fedor, self.masha])

    def test_ok_update_room(self):
        NEWNAMEROOM = 'Поэмы'
        new_users_pk = [self.roman.pk, self.fedor.pk]
        res = self.client.put(reverse('room-detail', kwargs={'room_id': self.room.id}), 
                              {'name': NEWNAMEROOM, 'users': new_users_pk})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], NEWNAMEROOM)
        self.assertEqual(res.data['users'], new_users_pk)
        self.assertEqual(res.data['id'], self.room.id)


class DeleteRoomTestCase(APITestCase):

    def setUp(self):
        self.artem = create_user('artem', is_staff=True)
        self.fedor = create_user('fedor')
        self.masha = create_user('masha')
        self.client.force_authenticate(user=self.artem)
        self.room_first = create_room('Природоведение', [self.fedor, self.masha])
        self.room_second = create_room('Красные цветы', [self.fedor, self.masha])

    def test_ok_delete_room(self):
        number_rooms = Room.objects.count()
        res = self.client.delete(reverse('room-detail', kwargs={'room_id': self.room_second.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Room.objects.count(), number_rooms - 1)
        delete_room = Room.objects.filter(id=self.room_second.id)
        self.assertEqual(len(delete_room), 0)