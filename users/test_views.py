from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from django.contrib.auth.models import User, Group
from . import views, serializers
from balarco import utils


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
        """Test that the API returns a valid token if credentials are correct.
        """
        url = reverse('users:api_login')
        data = {'username': 'juliannieb', 'password': 'juliannieb'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_do_not_return_authentication_token(self):
        """Test that the API doesn't return if credentials are incorrect.
        """
        url = reverse('users:api_login')
        data = {'username': 'juliannieb', 'password': 'incorrect_password'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetTest(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='marcoantonio',
            first_name='Marco',
            last_name='Lopez',
            email='marcolm485@gmail.com',
            password='marcolopez')
        User.objects.create_user(
            username='juliannieb',
            first_name='Julian',
            last_name='Niebieskikwiat',
            email='juliannieb@gmail.com',
            password='juliannieb')

    def test_send_reset_email(self):
        """Test that calling the resest password API returns a successful response.
        """
        url = reverse('users:api_reset_password')
        data = {'email': 'marcolm485@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_do_not_send_reset_email(self):
        """Test that calling the resest password API returns a failed response if mail doesn't exist.
        """
        url = reverse('users:api_reset_password')
        data = {'email': 'does_not_exist@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserRegistrationTest(APITestCase):
    def test_create_user(self):
        """Test that an object instance can be generated through the REST API endpoint.
        """
        url = reverse('users:api_registration')
        data = {
                'username': 'marcoantonio@gmail.com',
                'password': 'marcoantonio123456',
                'first_name': 'Marco',
                'last_name': 'Lopez',
                'email': 'marcoantonio@gmail.com'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_do_not_create_user(self):
        """Test that an object instance cannot be created without the complete information.
        """
        url = reverse('users:api_registration')
        data = {
                'first_name': 'Marco',
                'last_name': 'Lopez',
                'password': 'marcoantonio123456'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list users.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user@example.com',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user@example.com', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = User
        self.serializer_class = serializers.UserSerializer

        test_user_1 = User.objects.create_user(
            username='marcoantonio@example.com', first_name='Marco',
            last_name='Lopez', email='marcolm485@gmail.com',
            password='marcolopez')
        test_user_2 = User.objects.create_user(
            username='juliannieb@example.com', first_name='Julian',
            last_name='Niebieskikwiat', email='juliannieb@gmail.com',
            password='juliannieb')

        self.test_objects = [self.user, test_user_1, test_user_2]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'username': 'new_user@example.com',
            'password': 'new_user_password',
            }

        self.data_filtering_test = {
            'username': 'marcoantonio@example.com',
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'username': 'different_address@example.com',
            }

        self.edition_obj_idx = 0

        self.view = views.UserViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'users:users-list'
        self.url_detail = 'users:users-detail'
        self.factory = APIRequestFactory()


class GroupAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list groups.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user@example.com',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user@example.com', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = Group
        self.serializer_class = serializers.GroupSerializer

        test_group_1 = Group.objects.create(
            name='Group 1')
        test_group_2 = Group.objects.create(
            name='Group 2')

        self.test_objects = [test_group_1, test_group_2]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'name': 'Group 3'
            }

        self.data_filtering_test = {
            'name': 'Group 1',
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'name': 'Group 4',
            }

        self.edition_obj_idx = 0

        self.view = views.GroupViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'users:groups-list'
        self.url_detail = 'users:groups-detail'
        self.factory = APIRequestFactory()

    def test_delete_object(self):
        pass
