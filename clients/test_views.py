from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework import status

from .models import Client, Contact
from .views import ContactViewSet


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
            phone='4471172395',
            email='julian@elguandul.com',
            alternate_email='julio@hotmail.com',
            alternate_phone='26416231',
            client=self.client_instance_starbucks,
            is_active=True)

        self.contact_instance_hector = Contact.objects.create(
            name='Hector',
            last_name='Sanchez',
            phone='4426683012',
            email='hector@eldominio.com',
            alternate_email='elotro@eldominio.com',
            alternate_phone='5555555',
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
            'email': 'lobato.meeser.fernando@hotmail.com',
            'phone': '4424674323',
            'alternate_email': 'ferlobo93@hotmail.com',
            'alternate_phone': '2341631',
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
        for client in response.data:
            self.assertEqual(client['name'], Contact.objects.get(id=client['id']).name)

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
            Test that a client object can be modified.
        """
        data = {
            'name': 'Julian',
            'last_name': 'Niebieskikiwat',
            'email': 'julian@elguandul.com',
            'phone': '66666666',
            'alternate_email': 'julio@hotmail.com',
            'alternate_phone': '2341631',
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
        self.assertEqual(instance_update.phone, '66666666')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
