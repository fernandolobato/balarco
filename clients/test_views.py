from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from clients.models import Client, Contact
from clients.views import APIContact


class ContactTest(APITestCase):
	"""
		Tests to verify the basic usage of the REST API to create, modify and list contacts.
		@TODO: Token authentication is not yet enabled. Once it's enabled, the force_authenticate methods
		should recieve the user and token as params.
	"""

	def setUp(self):
		self.client_instance_starbucks = Client.objects.create(
			name='Test Starbucks',
			address='Felipe Ángeles 225')

		self.contact_instance_julian = Contact.objects.create(
			name='Julian',
			last_name='Niebieskikiwat',
			phone='4471172395',
			email='julian@elguandul.com',
			alternate_email='julio@hotmail.com',
			alternate_phone='26416231',
			client=self.client_instance_starbucks)

		self.contact_instance_hector = Contact.objects.create(
			name='Hector',
			last_name='Sanchez',
			phone='4426683012',
			email='hector@eldominio.com',
			alternate_email='elotro@eldominio.com',
			alternate_phone='5555555',
			client=self.client_instance_starbucks)

		self.number_of_contacts = 2
		self.url = 'clients:api_contact'
		self.factory = APIRequestFactory()
		self.view = APIContact.as_view()

	def test_contact_creation(self):
		"""
			Test that a client instance can be generated through the REST API endpoint.
		"""

		data = {
			'name': 'Fernando',
			'last_name': 'Lobato Meeser',
			'email': 'lobato.meeser.fernando@hotmail.com',
			'phone': '4424674323',
			'alternate_email': 'ferlobo93@hotmail.com',
			'alternate_phone': '2341631',
			'client': self.client_instance_starbucks.id}
		request = self.factory.post(reverse(self.url), data=data)
		force_authenticate(request)
		response = self.view(request)

		contact_instance = Contact.objects.get(id=response.data['id'])

		self.assertEqual('Fernando', contact_instance.name)
		self.assertEqual(self.number_of_contacts + 1, Contact.objects.all().count())

	def test_multiple_contact_listing(self):
		"""
			Tests that all client objects can be retrieved through the REST API endpoint.
		"""
		request = self.factory.get(reverse(self.url))
		force_authenticate(request)
		response = self.view(request)

		self.assertEqual(self.number_of_contacts, len(response.data))
		for client in response.data:
			self.assertEqual(client['name'], Contact.objects.get(id=client['id']).name)

	def test_empty_contact_creation(self):
		"""
			Tests that a client object can't be created without the required information.
		"""
		data = {}
		request = self.factory.post(reverse(self.url), data=data)
		force_authenticate(request)
		response = self.view(request)
		tags = ['name', 'last_name', 'email', 'client']
		for tag in tags:
			self.assertEqual(str(response.data[tag]), "['This field is required.']")
