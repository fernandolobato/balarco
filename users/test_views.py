from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User


class TokenCreationTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='marcoantonio', first_name='Marco',
            last_name='Lopez', email='marcolm485@gmail.com',
            password='marcolopez')
        User.objects.create_user(
            username='juliannieb', first_name='Julian',
            last_name='Niebieskikwiat', email='juliannieb@gmail.com',
            password='juliannieb')

    def test_return_authentication_token(self):
        url = reverse('users:api_login')
        data = {'username': 'juliannieb', 'password': 'juliannieb'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_authentication_token(self):
        url = reverse('users:api_login')
        data = {'username': 'juliannieb', 'password': 'incorrect_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='marcoantonio', first_name='Marco',
            last_name='Lopez', email='marcolm485@gmail.com',
            password='marcolopez')
        User.objects.create_user(
            username='juliannieb', first_name='Julian',
            last_name='Niebieskikwiat', email='juliannieb@gmail.com',
            password='juliannieb')

    def test_send_reset_email(self):
        url = reverse('users:api_reset_password')
        data = {'email: marcolm485@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
