from .models import Client, Contact
from .serializers import ClientSerializer, ContactSerializer
from balarco import utils
from rest_framework import viewsets


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet for Contact CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = Contact.objects.filter(is_active=True)
    serializer_class = ContactSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """ViewSet for Client CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = Client.objects.filter(is_active=True)
    serializer_class = ClientSerializer
