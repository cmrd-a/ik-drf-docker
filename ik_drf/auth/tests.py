from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView

from guestbook.models import User


class AuthTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.su_creds = {'username': 'newadmin', 'password': 'secretpass'}
        User.objects.create_superuser(**self.su_creds)

    def test_auth_login_wrong_creds(self):
        request = self.factory.post('/auth/login/', {'username': 'persona', 'password': 'non_grata'})
        response = TokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')

    def test_auth_login_success(self):
        request = self.factory.post('/auth/login/', self.su_creds)
        response = TokenObtainPairView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)


class AuthPersistTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.su_creds = {'username': 'superadmin', 'password': 'qwerty123'}
        User.objects.create_superuser(**self.su_creds)
        response = self.client.post('/auth/login/', self.su_creds)
        self.refresh_token = response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_auth_refresh(self):
        response = self.client.post(
            '/auth/login/refresh/',
            {'refresh': self.refresh_token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_auth_logout(self):
        response = self.client.post(
            '/auth/logout/',
            {'refresh_token': self.refresh_token},
        )
        self.assertEqual(response.status_code, 205)

    def test_auth_logout_all(self):
        response = self.client.post(
            '/auth/logout_all/',
            {'refresh_token': self.refresh_token},
        )
        self.assertEqual(response.status_code, 205)
