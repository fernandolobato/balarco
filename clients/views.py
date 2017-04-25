from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers as serializers_library
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Contact
from .serializers import ClientSerializer, ContactSerializer
from balarco import utils
from . import filters as client_filters
from works.models import Work


class ContactViewSet(utils.GenericViewSet):
    """ViewSet for Contact CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Contact
    queryset = Contact.objects.filter(is_active=True)
    serializer_class = ContactSerializer
    filter_class = client_filters.ContactFilter

    def destroy(self, request, pk=None):
        """Override of destroy method, with raises an exception when the selected
           contact to delete belongs to a work object via contact relationship
        """
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        work_queryset = Work.objects.filter(contact=obj)
        error_message = 'Antes de eliminar el contacto, reasigna todos sus proyectos'
        if work_queryset.count() > 0:
            raise serializers_library.ValidationError(error_message)
        else:
            obj.is_active = False
            try:
                obj.save()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            except:
                return Http404('No se pudo borrar el contacto en este momento')


class ClientViewSet(utils.GenericViewSet):
    """ViewSet for Client CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Client
    queryset = Client.objects.filter(is_active=True)
    serializer_class = ClientSerializer
    filter_class = client_filters.ClientFilter
