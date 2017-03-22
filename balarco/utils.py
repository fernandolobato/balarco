import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework.authtoken.models import Token


GROUP_DIR_CUENTAS = "Director de cuentas"
GROUP_EJECUTIVO = "Ejecutivo"
GROUP_VENTAS = "Ventas"
GROUP_DIR_ARTE = "Director de arte"
GROUP_DISENADOR_SR = "Diseñador SR"
GROUP_DISENADOR_JR = "Diseñador JR"
GROUP_SUPERUSUARIO = "Super usuario"


def generic_rest_soft_delete(request, serializer_class, obj_class, pk):
    """Function used by GenericViewSet:destroy to make a soft delete of the specified object.
    This means that the object is not truly deleted but its active state change to false.
    The object must be active to delete it.

    Parameters
    ----------
    request: request
        The request that was made by the client
    serializer_class: class
        Class of the model serializer
    obj_class: class
        Class of the model
    pk: int
        Id of the requested object

    Returns
    -------
    Response
        Response object containing the serializer data
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    obj.is_active = False
    obj.save()
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


class GenericViewSet(viewsets.ModelViewSet):
    """Generic view set for basic CRUD REST Service.
    To use it a ViewSet has to inherit from it and add the attributes.

    Attributes
    ----------
    obj_class: class
        Class of the main model that the REST is going to work on
    serializer_class: class
        Class of the serializer that is going to represent the obj_class
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    obj_class = None
    serializer_class = None
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)

    def destroy(self, request, pk=None):
        return generic_rest_soft_delete(request, self.serializer_class, self.obj_class, pk)


class GenericAPITest(APITestCase):
    """Tests to verify the basic usage of the REST API to create, modify and list objects.
    To use, a new class that inherits from utils.GenericAPITest has to be declared.
    The setUp function and its attributes must be overriden.

    Setup attributes
    ----------------
    self.user: User model object
        Test user created on the DB for authentication
    self.obj_class: Model class
        Model class of the API REST that's being tested
    self.test_objects:
        Array containing all the object_class objects created and saved in the test DB
    self.number_of_initial_objects: int
        Size of the test objects array->len(self.test_objects)
    self.data_creation_test: dict
        Dictionary containing necessary data to create an object succesfuly
    self.data_edition_test: dict
        Dictionary containing necessary data to edit an object succesfuly
    self.edition_obj_idx: int
        Index of the object in the array of objects that's going to be edited in the
        test with the data_edition_test dict.
    self.view: GenericViewSet
        GenericViewSet that's being tested with a dict of http methods.
        e.g:
        ObjectViewSet.as_view({
                    'get': 'list',
                    'post': 'create',
                    'put': 'update',
                    'patch': 'partial_update',
                    'delete': 'destroy'
                    })
    self.url_list: string
        Location of the viewset-list API without reversing it.
        e.g: 'app:objects-list'
    self.url_detail: string
        Location of the viewset-detail API without reversing it.
        e.g: 'app:objects-detail'
    self.factory: APIRequestFactory
        Factory to construct requests, it must be always = APIRequestFactory()
    """

    def setUp(self):
        self.user = None
        self.obj_class = None
        self.serializer_class = None
        self.test_objects = []
        self.number_of_initial_objects = 0
        self.data_creation_test = {}
        self.data_edition_test = {}
        self.edition_obj_idx = 0
        self.view = None
        self.url_list = ''
        self.url_detail = ''
        self.factory = APIRequestFactory()

    def test_object_creation(self):
        """Test that an object instance can be generated through the REST API endpoint.
        """
        request = self.factory.post(reverse(self.url_list), data=self.data_creation_test)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)

        object_instance = self.obj_class.objects.get(id=response.data['id'])
        serialized_object = self.serializer_class(object_instance)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key in self.data_creation_test.keys():
            if key in serialized_object:
                self.assertEqual(str(self.data_creation_test[key]), str(serialized_object[key]))
        self.assertEqual(self.number_of_initial_objects + 1, self.obj_class.objects.all().count())

    def test_multiple_object_listing(self):
        """Tests that all class objects can be retrieved through the REST API endpoint.
        """
        request = self.factory.get(reverse(self.url_list))
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.number_of_initial_objects, len(response.data))
        for obj in response.data:
            object_instance = self.obj_class.objects.get(id=obj['id'])
            serialized_object = self.serializer_class(object_instance)
            for key in obj.keys():
                if key in serialized_object:
                    self.assertEqual(str(obj[key]), str(serialized_object[key]))

    def test_filters(self):
        """Tests that all class objects can be filtered through the REST API endpoint.
        """
        request = self.factory.get(reverse(self.url_list), data=self.data_filtering_test)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.number_of_filtered_objects, len(response.data))
        for obj in response.data:
            object_instance = self.obj_class.objects.get(id=obj['id'])
            serialized_object = self.serializer_class(object_instance)
            for key in obj.keys():
                if key in serialized_object:
                    self.assertEqual(str(obj[key]), str(serialized_object[key]))

    def test_empty_object_creation(self):
        """Tests that an object can't be created without the required information.
        """
        data = {}
        request = self.factory.post(reverse(self.url_list), data=data)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_modify_object(self):
        """Test that an object can be modified.
        """
        edit_obj_instance = self.test_objects[self.edition_obj_idx]
        request = self.factory.patch(reverse(self.url_detail,
                                             kwargs={'pk': edit_obj_instance.id}),
                                     data=self.data_edition_test)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request, pk=edit_obj_instance.id)

        object_instance = self.obj_class.objects.get(id=edit_obj_instance.id)
        serialized_object = self.serializer_class(object_instance)
        for key in self.data_edition_test.keys():
            if key in serialized_object:
                self.assertEqual(str(self.data_edition_test[key]), str(serialized_object[key]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_object(self):
        """Test that an object can be deleted.
        """
        edit_obj_instance = self.test_objects[self.edition_obj_idx]
        request = self.factory.delete(reverse(self.url_detail,
                                              kwargs={'pk': edit_obj_instance.id}),
                                      data=self.data_edition_test)
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request, pk=edit_obj_instance.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        request = self.factory.get(reverse(self.url_list))
        token = Token.objects.get(user=self.user)
        force_authenticate(request, user=self.user, token=token)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.number_of_initial_objects - 1, len(response.data))
