from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from rest_framework.test import APIRequestFactory

from .models import Client, Contact
from .views import ContactViewSet, ClientViewSet
from . import serializers
from balarco import utils


class ContactTest(utils.GenericAPITest):
    """
        Tests to verify the basic usage of the REST API to create, modify and list contacts.
        It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = Contact
        self.serializer_class = serializers.ContactSerializer

        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        client_instance_starbucks = Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)

        contact_instance_julian = Contact.objects.create(
            name='Julian',
            last_name='Niebieskikiwat',
            charge='Manager',
            landline='4471172395',
            mobile_phone_1='26416231',
            email='julian@elguandul.com',
            alternate_email='julio@hotmail.com',
            client=client_instance_starbucks,
            is_active=True)

        contact_instance_hector = Contact.objects.create(
            name='Hector',
            last_name='Sanchez',
            charge='Developer',
            landline='4426683012',
            mobile_phone_1='5555555',
            email='hector@eldominio.com',
            client=client_instance_starbucks,
            is_active=True)

        self.test_objects = [contact_instance_julian, contact_instance_hector]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'name': 'Fernando',
            'last_name': 'Lobato Meeser',
            'charge': 'Project Owner',
            'landline': '4424674323',
            'mobile_phone_1': '2341631',
            'email': 'lobato.meeser.fernando@hotmail.com',
            'alternate_email': 'ferlobo93@hotmail.com',
            'client': client_instance_starbucks.id,
            'is_active': True
            }

        self.data_edition_test = {
            'name': 'Julian',
            'last_name': 'Niebieskikiwat',
            'charge': 'Manager',
            'landline': '66666666',
            'mobile_phone_1': '2341631',
            'email': 'julian@elguandul.com',
            'alternate_email': 'julio@hotmail.com',
            'client': client_instance_starbucks.id,
            'is_active': True
            }

        self.edition_obj_idx = 0

        self.view = ContactViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'clients:contacts-list'
        self.url_detail = 'clients:contacts-detail'
        self.factory = APIRequestFactory()


class ClientTest(utils.GenericAPITest):
    """
        Tests to verify the basic usage of the REST API to create, modify and list clients.
        It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')

        self.obj_class = Client
        self.serializer_class = serializers.ClientSerializer

        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        client_instance_starbucks = Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)

        client_instance_oxxo = Client.objects.create(
            name='OXXO',
            address='Epigmenio González 128',
            is_active=True)

        self.test_objects = [client_instance_starbucks, client_instance_oxxo]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'name': 'COMEX',
            'address': 'Calle 5 de Mayo 350',
            'is_active': True
            }

        self.data_edition_test = {
            'name': 'OXXO',
            'address': 'Bernardo Quintana 221',
            'is_active': True
            }

        self.edition_obj_idx = 1
        self.view = ClientViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'clients:clients-list'
        self.url_detail = 'clients:clients-detail'
        self.factory = APIRequestFactory()
