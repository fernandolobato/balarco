from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from . import models, serializers
from balarco import utils


class WorkTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for WorkType CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.WorkType.objects.filter(is_active=True)
    serializer_class = serializers.WorkTypeSerializer


class ArtTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for ArtType CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.ArtType.objects.filter(is_active=True)
    serializer_class = serializers.ArtTypeSerializer


class IgualaViewSet(viewsets.ModelViewSet):
    """ViewSet for Iguala CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.Iguala.objects.filter(is_active=True)
    serializer_class = serializers.IgualaSerializer


class ArtIgualaViewSet(viewsets.ModelViewSet):
    """ViewSet for ArtIguala CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.ArtIguala.objects.filter(is_active=True)
    serializer_class = serializers.ArtIgualaSerializer


class WorkViewSet(viewsets.ModelViewSet):
    """ViewSet for Work CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.Work.objects.filter(is_active=True)
    serializer_class = serializers.WorkSerializer

    @detail_route(methods=['get'], url_path='possible-status-changes')
    def possible_status_changes(self, request, pk=None):
        queryset = models.Work.objects.filter(is_active=True)
        work = get_object_or_404(queryset, pk=pk)
        possible_status_changes = work.get_possible_status_changes(request.user)
        serializer = serializers.StatusSerializer(possible_status_changes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class ArtWorkViewSet(viewsets.ModelViewSet):
    """ViewSet for ArtWork CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.ArtWork.objects.filter(is_active=True)
    serializer_class = serializers.ArtWorkSerializer


class FileViewSet(viewsets.ModelViewSet):
    """ViewSet for File CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.File.objects.filter(is_active=True)
    serializer_class = serializers.FileSerializer


class WorkDesignerViewSet(viewsets.ModelViewSet):
    """ViewSet for WorkDesigner CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.WorkDesigner.objects.filter(is_active=True)
    serializer_class = serializers.WorkDesignerSerializer


class StatusChangeViewSet(viewsets.ModelViewSet):
    """ViewSet for StatusChange CRUD REST Service that inherits from viewsets.ModelViewSet
    """
    queryset = models.StatusChange.objects.filter(is_active=True)
    serializer_class = serializers.StatusChangeSerializer
