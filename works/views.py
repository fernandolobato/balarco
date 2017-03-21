import django_filters.rest_framework
from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers
from . import filters as works_filters
from balarco import utils


class WorkTypeViewSet(utils.GenericViewSet):
    """ViewSet for WorkType CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.WorkType
    queryset = models.WorkType.objects.filter(is_active=True)
    serializer_class = serializers.WorkTypeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.WorkTypeFilter


class ArtTypeViewSet(utils.GenericViewSet):
    """ViewSet for ArtType CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtType
    queryset = models.ArtType.objects.filter(is_active=True)
    serializer_class = serializers.ArtTypeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.ArtTypeFilter


class IgualaViewSet(utils.GenericViewSet):
    """ViewSet for Iguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Iguala
    queryset = models.Iguala.objects.filter(is_active=True)
    serializer_class = serializers.IgualaSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.IgualaFilter

    def create(self, request):
        """Overrided method because an Iguala has a list of Art types associated.
        All objects are sended directly in the same WS and here are processed.
        A roll back is done in case of failure so it's an atomic function
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_obj = self.obj_class.objects.create(**serializer.validated_data)
            art_igualas = request.data['art_iguala']
            for art_iguala in art_igualas:
                art_iguala['iguala'] = new_obj.id
                serializer_art_iguala = serializers.ArtIgualaSerializer(data=art_iguala)
                if serializer_art_iguala.is_valid():
                    models.ArtIguala.objects.create(**serializer_art_iguala.validated_data)
                else:
                    query_art_iguala = models.ArtIguala.objects.filter(iguala=new_obj)
                    for art_iguala in query_art_iguala:
                        art_iguala.delete()
                    new_obj.delete()
                    return Response({
                        'status': 'Bad request',
                        'message': '%s could not be created with received data.' %
                                   self.obj_class.__name__
                    }, status=status.HTTP_400_BAD_REQUEST)
            return Response(self.serializer_class(new_obj).data, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': '%s could not be created with received data.' % self.obj_class.__name__
        }, status=status.HTTP_400_BAD_REQUEST)


class ArtIgualaViewSet(utils.GenericViewSet):
    """ViewSet for ArtIguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtIguala
    queryset = models.ArtIguala.objects.filter(is_active=True)
    serializer_class = serializers.ArtIgualaSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.ArtIgualaFilter


class WorkViewSet(utils.GenericViewSet):
    """ViewSet for Work CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Work
    queryset = models.Work.objects.filter(is_active=True)
    serializer_class = serializers.WorkSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.WorkFilter

    @detail_route(methods=['get'], url_path='possible-status-changes')
    def possible_status_changes(self, request, pk=None):
        queryset = models.Work.objects.filter(is_active=True)
        work = get_object_or_404(queryset, pk=pk)
        possible_status_changes = work.get_possible_status_changes(request.user)
        serializer = serializers.StatusSerializer(possible_status_changes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ArtWorkViewSet(utils.GenericViewSet):
    """ViewSet for ArtWork CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtWork
    queryset = models.ArtWork.objects.filter(is_active=True)
    serializer_class = serializers.ArtWorkSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.ArtWorkFilter


class FileViewSet(utils.GenericViewSet):
    """ViewSet for File CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.File
    queryset = models.File.objects.filter(is_active=True)
    serializer_class = serializers.FileSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.FileFilter


class WorkDesignerViewSet(utils.GenericViewSet):
    """ViewSet for WorkDesigner CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.WorkDesigner
    queryset = models.WorkDesigner.objects.filter(is_active=True)
    serializer_class = serializers.WorkDesignerSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.WorkDesignerFilter


class StatusChangeViewSet(utils.GenericViewSet):
    """ViewSet for StatusChange CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.StatusChange
    queryset = models.StatusChange.objects.filter(is_active=True)
    serializer_class = serializers.StatusChangeSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_class = works_filters.StatusChangeFilter
