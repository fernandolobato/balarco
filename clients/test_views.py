from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status

from .models import Client, Contact
from .views import ContactViewSet, ClientViewSet


class ContactTest(APITestCase):
    """
        Tests to verify the basic usage of the REST API to create, modify and list contacts.
        @TODO: Token authentication is not yet enabled. Once it's enabled, the
        force_authenticate methods should recieve the user and token as params.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')

        self.client_instance_starbucks = Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)

        self.contact_instance_julian = Contact.objects.create(
            name='Julian',
            last_name='Niebieskikiwat',
            charge='Manager',
            landline='4471172395',
            mobile_phone_1='26416231',
            email='julian@elguandul.com',
            alternate_email='julio@hotmail.com',
            client=self.client_instance_starbucks,
            is_active=True)

        self.contact_instance_hector = Contact.objects.create(
            name='Hector',
            last_name='Sanchez',
            charge='Developer',
            landline='4426683012',
            mobile_phone_1='5555555',
            email='hector@eldominio.com',
            client=self.client_instance_starbucks,
            is_active=True)

        self.number_of_contacts = 2
        self.url_list = 'clients:Contacts-list'
        self.url_detail = 'clients:Contacts-detail'
        self.factory = APIRequestFactory()

    def test_contact_creation(self):
        """
            Test that a contact instance can be generated through the REST API endpoint.
        """
        data = {
            'name': 'Fernando',
            'last_name': 'Lobato Meeser',
            'charge': 'Project Owner',
            'landline': '4424674323',
            'mobile_phone_1': '2341631',
            'email': 'lobato.meeser.fernando@hotmail.com',
            'alternate_email': 'ferlobo93@hotmail.com',
            'client': self.client_instance_starbucks.id,
            'is_active': True}
        request = self.factory.post(reverse(self.url_list), data=data)
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({
                                      'post': 'create',
                                      })
        response = view(request)
        contact_instance = Contact.objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('Fernando', contact_instance.name)
        self.assertEqual(self.number_of_contacts + 1, Contact.objects.all().count())

    def test_multiple_contact_listing(self):
        """
            Tests that all contact objects can be retrieved through the REST API endpoint.
        """
        request = self.factory.get(reverse(self.url_list))
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({
                                      'get': 'list',
                                      })
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.number_of_contacts, len(response.data))
        for contact in response.data:
            self.assertEqual(contact['name'], Contact.objects.get(id=contact['id']).name)

    def test_empty_contact_creation(self):
        """
            Tests that a contact object can't be created without the required information.
        """
        data = {}
        request = self.factory.post(reverse(self.url_list), data=data)
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({
                                      'post': 'create',
                                      })
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_contact(self):
        """
            Test that a contact object can be modified.
        """
        data = {
            'name': 'Julian',
            'last_name': 'Niebieskikiwat',
            'charge': 'Manager',
            'landline': '66666666',
            'mobile_phone_1': '2341631',
            'email': 'julian@elguandul.com',
            'alternate_email': 'julio@hotmail.com',
            'client': self.client_instance_starbucks.id,
            'is_active': True
            }
        request = self.factory.put(reverse(self.url_detail,
                                           kwargs={'pk': self.contact_instance_julian.id}),
                                   data=data)
        force_authenticate(request, user=self.user)
        view = ContactViewSet.as_view({
                                      'put': 'update',
                                      })
        response = view(request, pk=self.contact_instance_julian.id)

        instance_update = Contact.objects.get(id=self.contact_instance_julian.id)
        self.assertEqual(instance_update.landline, '66666666')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ClientTest(APITestCase):
    """
        Tests to verify the basic usage of the REST API to create, modify and list clients.
        @TODO: Token authentication is not yet enabled. Once it's enabled, the
        force_authenticate methods should recieve the user and token as params.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')

        self.client_instance_starbucks = Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)

        self.client_instance_oxxo = Client.objects.create(
            name='OXXO',
            address='Epigmenio González 128',
            is_active=True)

        self.number_of_clients = 2
        self.url_list = 'clients:Clients-list'
        self.url_detail = 'clients:Clients-detail'
        self.factory = APIRequestFactory()

    def test_client_creation(self):
        """
            Test that a client instance can be generated through the REST API endpoint.
        """

        data = {
            'name': 'COMEX',
            'address': 'Calle 5 de Mayo 350',
            'is_active': True}
        request = self.factory.post(reverse(self.url_list), data=data)
        force_authenticate(request, user=self.user)
        view = ClientViewSet.as_view({
                                      'post': 'create',
                                      })
        response = view(request)
        client_instance = Client.objects.get(id=response.data['id'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual('COMEX', client_instance.name)
        self.assertEqual(self.number_of_clients + 1, Client.objects.all().count())

    def test_multiple_client_listing(self):
        """
            Tests that all client objects can be retrieved through the REST API endpoint.
        """
        request = self.factory.get(reverse(self.url_list))
        force_authenticate(request, user=self.user)
        view = ClientViewSet.as_view({
                                      'get': 'list',
                                      })
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.number_of_clients, len(response.data))
        for client in response.data:
            self.assertEqual(client['name'], Client.objects.get(id=client['id']).name)

    def test_empty_client_creation(self):
        """
            Tests that a client object can't be created without the required information.
        """
        data = {}
        request = self.factory.post(reverse(self.url_list), data=data)
        force_authenticate(request, user=self.user)
        view = ClientViewSet.as_view({
                                      'post': 'create',
                                      })
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_contact(self):
        """
            Test that a client object can be modified.
        """
        data = {
            'name': 'OXXO',
            'address': 'Bernardo Quintana 221',
            'is_active': True
            }
        request = self.factory.put(reverse(self.url_detail,
                                           kwargs={'pk': self.client_instance_oxxo.id}),
                                   data=data)
        force_authenticate(request, user=self.user)
        view = ClientViewSet.as_view({
                                      'put': 'update',
                                      })
        response = view(request, pk=self.client_instance_oxxo.id)

        instance_update = Client.objects.get(id=self.client_instance_oxxo.id)
        self.assertEqual(instance_update.address, 'Bernardo Quintana 221')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
