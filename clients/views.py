from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from clients.models import Client, Contact
from clients.serializers import ClientSerializer, ClientSerializerComplete, ContactSerializer


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
        queryset = Client.objects.filter(is_active=True)
        serializer = ClientSerializerComplete(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            Client.objects.create(**serializer.validated_data)
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Client could not be created with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Client.objects.all()
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializerComplete(client)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Client.objects.filter(is_active=True)
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status': 'Bad request',
            'message': 'Client could not be updated with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        queryset = Client.objects.filter(is_active=True)
        client = get_object_or_404(queryset, pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({
            'status': 'Bad request',
            'message': 'Client could not be updated with received data.'
        }, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Client.objects.filter(is_active=True)
        client = get_object_or_404(queryset, pk=pk)
        client.is_active = False
        client.save()
        delete_queryset(Contact.objects.filter(client=client))
        serializer = ClientSerializerComplete(queryset, many=True)
        return Response(serializer.data)
