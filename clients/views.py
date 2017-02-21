from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from clients.models import Client, Contact
from clients.serializers import ClientSerializer, ContactSerializer
from balarco import utils


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


class ClientViewSet(utils.GenericViewSet):
    """
    
    """

    obj_class = Client
    serializer_class = ClientSerializer
