from django.test import TestCase
from .models import Client

class ClientTestCase(TestCase):
    def setUp(self):
        Client.objects.create(name="Test Starbucks", address="Felipe Ángeles 225")
        Client.objects.create(name="Test OXXO", address="Reforma 190")

    def test_client_names(self):
        """The objects are created and their __str__ func works"""
        starbucks = Client.objects.get(name="Test Starbucks")
        oxxo = Client.objects.get(name="Test OXXO")
        self.assertEqual(str(starbucks), 'Test Starbucks')
        self.assertEqual(str(oxxo), 'Test OXXO')
