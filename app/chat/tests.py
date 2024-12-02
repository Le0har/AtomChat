from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from chat.models import Message, Room


User = get_user_model()


class CreatingUser():

    def create_new_user(self, data):
        self.user = User.objects.create(**data)
        self.user.set_password(data['password'])
        self.user.save()


class RegisterTestCase(APITestCase):

    def test_ok_create_user(self):
        number_records = User.objects.count()
        res = self.client.post(reverse('users-list'), {'username': 'michael', 'password': 'user_mic1987'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), number_records + 1)
        new_user = User.objects.get(username='michael')
        self.assertEqual(new_user.username, 'michael')
        self.assertEqual(new_user.is_active, True)


class LoginTestCase(APITestCase, CreatingUser): 

    def setUp(self):
        self.data = {'username': 'tamara', 'password': 'user_tam1971'}
        self.create_new_user(self.data)

    def test_ok_create_token(self):
        res = self.client.post(reverse('get-token'), self.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_token = res.data['token']
        user_by_token = Token.objects.get(key=new_token).user
        self.assertEqual(user_by_token.username, 'tamara')


class MessageTestCase(APITestCase, CreatingUser):

    def setUp(self):
        self.data_ruslan = {'username': 'ruslan', 'password': 'user_rusl1983'}
        self.data_ludmila = {'username': 'ludmila', 'password': 'user_ludm1982'}
        self.create_new_user(self.data_ruslan)
        self.create_new_user(self.data_ludmila)

    def test_ok_send_message(self):
        ruslan = User.objects.get(username=self.data_ruslan['username'])
        ludmila = User.objects.get(username=self.data_ludmila['username'])
        self.client.force_authenticate(user=ruslan)
        number_messages = Message.objects.count()
        number_rooms = Room.objects.count()
        res = self.client.post(reverse('message-list'), {'text': 'Привет, как дела?', 'user_to': ludmila.pk})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), number_messages + 1)
        new_message = Message.objects.get(text='Привет, как дела?')
        self.assertEqual(new_message.text, 'Привет, как дела?')
        self.assertEqual(new_message.author, ruslan)
        self.assertEqual(Room.objects.count(), number_rooms + 1)
        new_room = Room.objects.get(name=f'{ruslan}&{ludmila}_private')
        self.assertEqual(new_room.name, 'ruslan&ludmila_private')
        self.assertEqual(new_room.is_private, True)
        users_in_room = new_room.users.all()
        self.assertEqual(users_in_room.count(), 2)
        self.assertEqual([*users_in_room], [ruslan, ludmila])
        

