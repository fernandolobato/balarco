from django.test import TestCase
from django.db import IntegrityError
from .models import User


class UserTest(TestCase):
    def setUp(self):
        User.objects.create_user(
            username='marcoantonio', first_name='Marco', last_name='Lopez',
            email='marcolm485@gmail.com', password='marcolopez')
        User.objects.create_user(
            username='juliannieb', first_name='Julian', last_name='Niebieskikwiat',
            email='juliannieb@gmail.com', password='juliannieb')

    def test_username(self):
        user_marco = User.objects.get(username='marcoantonio')
        user_julian = User.objects.get(username='juliannieb')
        self.assertEqual(user_marco.first_name, 'Marco')
        self.assertEqual(user_julian.first_name, 'Julian')

    def test_creation(self):
        current_user_count = len(User.objects.all())
        User.objects.create(username='eduardovaca', first_name='Eduardo', last_name='Vaca',
                            email='vacalalo@gmail.com', password='eduardovaca')
        expected_user_count = current_user_count + 1
        current_user_count = len(User.objects.all())
        self.assertEqual(current_user_count, expected_user_count)

    def test_deletion(self):
        current_user_count = len(User.objects.all())
        user_eduardo = User.objects.get(username='marcoantonio')
        user_eduardo.delete()
        expected_user_count = current_user_count - 1
        current_user_count = len(User.objects.all())
        self.assertEqual(current_user_count, expected_user_count)

    def test_update(self):
        user_marco = User.objects.get(username='marcoantonio')
        user_marco.last_name = 'Morales'
        self.assertEqual(user_marco.last_name, 'Morales')

    def test_unique_username(self):
        User.objects.create(username='eduardovaca', first_name='Eduardo', last_name='Vaca',
                            email='vacalalo@gmail.com', password='eduardovaca')
        with self.assertRaises(IntegrityError):
            User.objects.create(username='eduardovaca', first_name='Eduardo', last_name='Vaca',
                                email='vacalalo@gmail.com', password='eduardovaca')