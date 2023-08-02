import json

from django.test import TestCase, Client
from rest_framework.authtoken.models import Token

from users.models import User


class TestUserAPI(TestCase):
    def test_signup_user(self):
        data = {
            'name': 'Alla',
            'email': 'alla@alla.com',
            'password': 'AllaAllaAlla121212'
        }

        c = Client()

        response = c.post('/api/users/signup/', data=data)

        self.assertEquals(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn('user', data.keys())
        self.assertIn('token', data.keys())

    def test_login(self):
        c = Client()
        us = User.objects.create(name='Alla',
                                 email='alla@alla.com')
        us.set_password('AllaAllaAlla121212')
        us.save()
        token = Token.objects.create(user=us)

        response = c.post('/api/users/login/', data={
            'username': 'alla@alla.com',
            'password': 'AllaAllaAlla121212'
        }, content_type='application/json')
        data = json.loads(response.content)


        self.assertEquals(response.status_code, 200)
        self.assertEquals(token.key, data['token'])



    def test_email_exist_error(self):
        us1 = User.objects.create(name='Alla',
                                  password='AllaAllaAlla12121212121',
                                  email='alla@alla.com')
        us1.set_password('AllaAllaAlla12121212121')
        us1.save()
        data2 = {
            'name': 'Alla1212',
            'email': 'alla@alla.com',
            'password': 'AllaAllaAlla121212qweqw'
        }

        c = Client()
        response = c.post('/api/users/signup/', data=data2)

        self.assertEquals(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "email": [
                "User with this email exists"
            ]
        })

    def test_failed_authentication(self):
        us1 = User.objects.create(name='Alla',
                                  password='AllaAllaAlla12121212121',
                                  email='alla@alla.com')
        us1.set_password('AllaAllaAlla12121212121')
        us1.save()

        c = Client()

        response = c.post('/api/users/login/', data={
            'username': 'alla@alla.com',
            'password': '121212'
        }, content_type='application/json')

        self.assertEquals(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data, {
            "non_field_errors": [
                "Unable to log in with provided credentials."
            ]
        })

    def test_users_list(self):
        c = Client()
        response = c.get('/api/users/list/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 0)

        data1 = {
            'name': 'Alla',
            'email': 'alla@alla.com',
            'password': 'AllaAllaAlla121212'
        }

        c.post('/api/users/signup/', data=data1)

        response = c.get('/api/users/list/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
