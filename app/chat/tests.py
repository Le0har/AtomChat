from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


User = get_user_model()

class RegisterTestCase(APITestCase):

    def test_ok_create_user(self):
        res = self.client.post(reverse('users-list'), {'username': 'tamara88', 'password': 'user_tam1987'})
        #print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase): 

    def setUp(self):
        self.login_request = {'username': 'tamara71', 'password': 'user_tam1971'}

        self.user = User.objects.create(**self.login_request)
        self.user.set_password(self.login_request['password'])

    def test_ok_login(self):
        res = self.client.post(reverse('get-token'), self.login_request)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)