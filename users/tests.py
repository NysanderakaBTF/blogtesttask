import json

from django.test import TestCase, Client
from rest_framework.authtoken.models import Token

from users.models import User


class TestUserAPI(TestCase):
    """
       Test class for User API endpoints.

       This class contains test cases for user signup, login, email existence error, failed authentication,
       and fetching the list of users.

       Usage:
       - Run the tests using a test runner (e.g., `python manage.py test`).

       """

    def test_signup_user(self):
        # Test user signup functionality.
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
        # Test user signup functionality.
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
        # Test handling of email existence error during signup.
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
        # Test handling of failed authentication.
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
        # Test fetching the list of users.
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
