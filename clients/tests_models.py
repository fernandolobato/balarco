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

class ContactTestCase(ClientTestCase):

	def setUp(self):
		starbucks = Client.objects.create(name='Test Starbucks', address='Felipe Ángeles 225')
		Client.objects.create(name='Test OXXO', address='Reforma 190')

		Contact.objects.create(
			name='Fernando',
			last_name='Lobato Meeser',
			phone='4424674323',
			email='lobato.meeser.fernando@hotmail.com',
			alternate_email='ferlobo93@hotmail.com',
			alternate_phone='2341631',
			client = starbucks)

	def test_contact_name(self):
		'''
    		Tests if the objects are being created in the database and their __str__ func works
    	'''
		client_instance = Contact.objects.get(name='Fernando')
		self.assertEqual(str(client_instance), 'Fernando Lobato Meeser')

	def test_relation_contact(self):
		'''
			Test if the contact objects are correctly referecing their clients.
		'''
		client_instance = Contact.objects.get(name='Fernando')
		starbucks = Client.objects.get(name='Test Starbucks')
		self.assertEqual(client_instance.client, starbucks)
