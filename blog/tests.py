import json

from django.test import TestCase, Client
from rest_framework import status
from rest_framework.authtoken.models import Token

from blog.models import Post
from users.models import User


class TestPostAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(name='Alla',
                                        email='alla@alla.who')
        cls.user1.set_password('123ALLAalla')
        cls.user1.save()

        cls.user2 = User.objects.create(name='Who',
                                        email='who@alla.who')
        cls.user2.set_password('123ALLAalla')
        cls.user2.save()

        cls.token1 = Token.objects.create(user=cls.user1)
        cls.token2 = Token.objects.create(user=cls.user2)

    def test_get_users_posts(self):
        c = Client()
        resp = c.get(f'/api/posts/user/{self.user1.pk}/')
        data = json.loads(resp.content)

        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(data), 0)

        post = Post.objects.create(author_id=self.user1.pk,
                                   title='Post 1',
                                   body='ALLLA')

        resp = c.get(f'/api/posts/user/{self.user1.pk}/')
        data = json.loads(resp.content)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['title'], 'Post 1')

    def test_create_post_unauthenticated(self):
        c = Client()
        resp = c.post('/api/posts/', data={
            'title': 'Post 1',
            'body': 'ALLLA'
        }, content_type='application/json')

        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authenticated(self):
        c = Client()
        resp = c.post('/api/posts/', data={
            'title': 'Post 1',
            'body': 'ALLLA'
        }, content_type='application/json', headers={'Authorization': f'Token {self.token1.key}'})

        self.assertEquals(resp.status_code, status.HTTP_201_CREATED)
        data = json.loads(resp.content)

        self.assertEquals(data['title'], 'Post 1')
        self.assertEquals(data['author'], self.user1.pk)

    def test_delete_post_unauthentticated(self):
        post = Post.objects.create(author_id=self.user1.pk,
                                   title='Post 1',
                                   body='ALLLA')

        c = Client()
        resp = c.delete(f'/api/posts/{post.pk}/')

        self.assertEquals(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_non_extisting_post(self):
        c = Client()
        resp = c.delete('/api/posts/1000/', headers={'Authorization':f'Token {self.token1.key}'})

        self.assertEquals(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_my_post(self):
        post = Post.objects.create(author_id=self.user1.pk,
                                   title='Post 1',
                                   body='ALLLA')
        self.assertEquals(Post.objects.filter(author_id=self.user1.pk).count(),
                          1)

        c = Client()
        resp = c.delete(f'/api/posts/{post.pk}/',
                        headers={'Authorization':f'Token {self.token1.key}'})

        self.assertEquals(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEquals(Post.objects.filter(author_id=self.user1.pk).count(),
                          0)

    def test_delete_not_my_post(self):
        post = Post.objects.create(author_id=self.user1.pk,
                                   title='Post 1',
                                   body='ALLLA')

        c = Client()
        resp = c.delete(f'/api/posts/{post.pk}/',
                        headers={'Authorization': f'Token {self.token2.key}'})
        self.assertEquals(resp.status_code, status.HTTP_403_FORBIDDEN)


