from rest_framework.generics import ListCreateAPIView
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from clients.models import Client, Contact
from clients.serializers import ClientSerializer, ContactSerializer


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

    def list(self, request):
        queryset = Client.objects.all()
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
