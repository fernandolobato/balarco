from .models import Client, Contact
from .serializers import ClientSerializer, ContactSerializer
from balarco import utils


class ContactViewSet(utils.GenericViewSet):
    """ViewSet for Contact CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Contact
    queryset = Contact.objects.filter(is_active=True)
    serializer_class = ContactSerializer


class ClientViewSet(utils.GenericViewSet):
    """ViewSet for Client CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Client
    queryset = Client.objects.filter(is_active=True)
    serializer_class = ClientSerializer
