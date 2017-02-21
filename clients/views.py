from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from clients.models import Client, Contact
from clients.serializers import ClientSerializer, ContactSerializer


def generic_rest_list_objects(request, serializer_class, obj_class):
    queryset = obj_class.objects.filter(is_active=True)
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)


def generic_rest_create_object(request, serializer_class, obj_class):
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        obj_class.objects.create(**serializer.validated_data)
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be created with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_retrieve_object(request, serializer_class, obj_class, pk):
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj)
    return Response(serializer.data)


def generic_rest_update_object(request, serializer_class, obj_class, pk, partial_update):
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj, data=request.data, partial=partial_update)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be updated with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_soft_delete(request, serializer_class, obj_class, pk):
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    obj.is_active = False
    obj.save()
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)


def delete_queryset(queryset):
    for obj in queryset:
        obj.is_active = False
        obj.save()


class APIContact(ListCreateAPIView):
    """
        API view to create, list or edit client.
        @TODO: Change permissions to isAuthenticated once tokens are enables.
        This Controller allows a user to consume and create information from
        contacts through a REST API using JSON format.
        Parameters
        ----------
        contact : int (optional)
            Can return a single instnce of an object instead of a complete query.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = ContactSerializer

    def get_queryset(self):
        queryset = Contact.objects.filter(is_active=True)

        if 'contact' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['contact'])

        return queryset


class ClientViewSet(viewsets.ViewSet):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = ClientSerializer

    def list(self, request):
        return generic_rest_list_objects(request, self.serializer_class, Client)

    def create(self, request):
        return generic_rest_create_object(request, self.serializer_class, Client)

    def retrieve(self, request, pk=None):
        return generic_rest_retrieve_object(request, self.serializer_class, Client, pk)

    def update(self, request, pk=None):
        return generic_rest_update_object(request, self.serializer_class, Client, pk, False)

    def partial_update(self, request, pk=None):
        return generic_rest_update_object(request, self.serializer_class, Client, pk, True)

    def destroy(self, request, pk=None):
        queryset = Client.objects.filter(is_active=True)
        client = get_object_or_404(queryset, pk=pk)
        delete_queryset(Contact.objects.filter(client=client))
        return generic_rest_soft_delete(request, self.serializer_class, Client, pk)
