from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from .models import Like, User, Entry
from .views import LikeView


class GuestbookPublicTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_likes_get(self):
        response = self.client.get('/likes/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_entries_get(self):
        response = self.client.get('/entries/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('created_at', response.data['results'][0])

    def test_entries_retrieve(self):
        response = self.client.get('/entries/1/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('created_at', response.data)


class GuestbookCommonUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_creds = {'username': 'commonuser', 'password': 'qwerty123'}
        User.objects.create_user(**self.user_creds)
        response = self.client.post('/auth/login/', self.user_creds)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_etries_post(self):
        response = self.client.post('/entries/', {'text': 'some_text'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['text'], 'some_text')
        self.assertEqual(response.data['user'], self.user_creds['username'])

    def test_entries_get(self):
        response = self.client.get('/entries/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('created_at', response.data['results'][0])

    def test_entries_retrieve_(self):
        response = self.client.get('/entries/1/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('created_at', response.data)

    def test_likes_post(self):
        response = self.client.post('/likes/', {'entry': 1})
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/likes/', {'entry': 1})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['non_field_errors'][0], 'Your like for this post already exists.')


class GuestbookSuperUserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_creds = {'username': 'superuser', 'password': 'qwerty123'}
        User.objects.create_superuser(**self.user_creds)
        response = self.client.post('/auth/login/', self.user_creds)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_get_entries(self):
        response = self.client.get('/entries/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('created_at', response.data['results'][0])

    def test_retrieve_entry(self):
        response = self.client.get('/entries/1/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('created_at', response.data)
