from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token


STATUS = (
    (0, 'Diseño'),
    (1, 'No'),
    (2, 'Unknown'),
)


def generic_rest_list_objects(request, serializer_class, obj_class):
    """
    Function to list all objects of a model in GenericViewSet:list.
    It makes a Query to the specified object class geting all active objects
    """
    queryset = obj_class.objects.filter(is_active=True)
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


def generic_rest_create_object(request, serializer_class, obj_class):
    """
    Function used in GenericViewSet:create to create and save a
    new object of the specified class.
    """
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        new_obj = obj_class.objects.create(**serializer.validated_data)
        return Response(serializer_class(new_obj).data, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be created with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_retrieve_object(request, serializer_class, obj_class, pk):
    """
    Function used by GenericViewSet:retrieve to retrieve the data of specified object.
    The object must be active to get it.
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj)
    return Response(serializer.data, status.HTTP_200_OK)


def generic_rest_update_object(request, serializer_class, obj_class, pk, partial_update):
    """
    Function used by GenericViewSet:update and GenericViewSet:partial_update to edit
    the data of the specified object.
    It receives a boolean called partial_update depending on which type of request is being
    handled (PUT/PATCH).
    The object must be active to edit it.
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj, data=request.data, partial=partial_update)
    if serializer.is_valid():
        updated_obj = serializer.save()
        return Response(serializer_class(updated_obj).data, status.HTTP_200_OK)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be updated with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_soft_delete(request, serializer_class, obj_class, pk):
    """
    Function used by GenericViewSet:destroy to make a soft delete of the specified object.
    This means that the object is not truly deleted but its active state change to false.
    The object must be active to delete it.
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    obj.is_active = False
    obj.save()
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


class GenericViewSet(viewsets.ViewSet):
    """
    Generic view set for basic CRUD REST Service.

    To use it a ViewSet has to inherit from it and add the attributes:
    obj_class: The model class
        Class of the main model that the REST is going to work on
    serializer_class: The serializer class of the model
        Class of the serializer that is going to represent the obj_class
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    obj_class = None
    serializer_class = None

    def list(self, request):
        return generic_rest_list_objects(request, self.serializer_class, self.obj_class)

    def create(self, request):
        return generic_rest_create_object(request, self.serializer_class, self.obj_class)

    def retrieve(self, request, pk=None):
        return generic_rest_retrieve_object(request, self.serializer_class, self.obj_class, pk)

    def update(self, request, pk=None):
        return generic_rest_update_object(request, self.serializer_class,
                                          self.obj_class, pk, False)

    def partial_update(self, request, pk=None):
        return generic_rest_update_object(request, self.serializer_class, self.obj_class, pk, True)

    def destroy(self, request, pk=None):
        return generic_rest_soft_delete(request, self.serializer_class, self.obj_class, pk)


class GenericAPITest(APITestCase):
    """
        Tests to verify the basic usage of the REST API to create, modify and list objects.
        To use, a new class that inherits from utils.GenericAPITest has to be declared.
        The setUp function and its attributes must be overriden:
            -self.user: test user created on the DB for authentication
            -self.obj_class: model class of the API REST that's being tested
            -self.test_objects: array containing all the object_class objects
                    created and saved in the test DB
            -self.number_of_initial_objects: size of the test objects array->len(self.test_objects)
            -self.data_creation_test: dictionary containing necessary data to create an object
                    succesfuly
            -self.data_edition_test: dictionary containing necessary data to edit an object
                    succesfuly
            -self.edition_obj_idx: index of the object in the array of objects
                    that's going to be edited in the test with the data_edition_test dict.
            -self.view: GenericViewSet that's being tested with a dict of http methods. Example:
                    ObjectViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })
            -self.url_list: location of the viewset-list API without reversing it.
                    Example: 'app:objects-list'
            -self.url_detail: location of the viewset-detail API without reversing it.
                    Example: 'app:objects-detail'
            -self.factory: factory to construct requests, it must be always = APIRequestFactory()
    """

    def setUp(self):
        self.user = None
        self.obj_class = None
        self.test_objects = []
        self.number_of_initial_objects = 0
        self.data_creation_test = {}
        self.data_edition_test = {}
        self.edition_obj_idx = 0
        self.view = None
        self.url_list = ''
        self.url_detail = ''
        self.factory = APIRequestFactory()

    def test_contact_creation(self):
        """
            Test that an object instance can be generated through the REST API endpoint.
        """
        request = self.factory.post(reverse(self.url_list), data=self.data_creation_test)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)

        object_instance = self.obj_class.objects.get(id=response.data['id'])
        object_instance_dict = model_to_dict(object_instance)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in self.data_creation_test.keys():
            if key in object_instance_dict:
                self.assertEqual(self.data_creation_test[key], object_instance_dict[key])
        self.assertEqual(self.number_of_initial_objects + 1, self.obj_class.objects.all().count())

    def test_multiple_contact_listing(self):
        """
            Tests that all class objects can be retrieved through the REST API endpoint.
        """
        request = self.factory.get(reverse(self.url_list))
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.number_of_initial_objects, len(response.data))
        for obj in response.data:
            object_instance = self.obj_class.objects.get(id=obj['id'])
            object_instance_dict = model_to_dict(object_instance)
            for key in obj.keys():
                if key in object_instance_dict:
                    self.assertEqual(obj[key], object_instance_dict[key])

    def test_empty_contact_creation(self):
        """
            Tests that an object can't be created without the required information.
        """
        data = {}
        request = self.factory.post(reverse(self.url_list), data=data)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_contact(self):
        """
            Test that an object can be modified.
        """
        edit_obj_instance = self.test_objects[self.edition_obj_idx]
        request = self.factory.put(reverse(self.url_detail,
                                           kwargs={'pk': edit_obj_instance.id}),
                                   data=self.data_edition_test)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request, pk=edit_obj_instance.id)

        object_instance = self.obj_class.objects.get(id=edit_obj_instance.id)
        object_instance_dict = model_to_dict(object_instance)
        for key in self.data_edition_test.keys():
            if key in object_instance_dict:
                self.assertEqual(self.data_edition_test[key], object_instance_dict[key])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
