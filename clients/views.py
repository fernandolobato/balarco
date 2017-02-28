from .models import Client, Contact
from .serializers import ClientSerializer, ContactSerializer
from balarco import utils


class ContactViewSet(utils.GenericViewSet):
    """
    ViewSet for Contact CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Contact
    serializer_class = ContactSerializer


class ClientViewSet(utils.GenericViewSet):
    """
    ViewSet for Client CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Client
    serializer_class = ClientSerializer
