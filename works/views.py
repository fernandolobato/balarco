from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from . import models, serializers
from . import filters as works_filters
from balarco import utils


class WorkTypeViewSet(utils.GenericViewSet):
    """ViewSet for WorkType CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.WorkType
    queryset = models.WorkType.objects.filter(is_active=True)
    serializer_class = serializers.WorkTypeSerializer
    filter_class = works_filters.WorkTypeFilter


class ArtTypeViewSet(utils.GenericViewSet):
    """ViewSet for ArtType CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtType
    queryset = models.ArtType.objects.filter(is_active=True)
    serializer_class = serializers.ArtTypeSerializer
    filter_class = works_filters.ArtTypeFilter


class IgualaViewSet(utils.GenericViewSet):
    """ViewSet for Iguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Iguala
    queryset = models.Iguala.objects.filter(is_active=True)
    serializer_class = serializers.IgualaSerializer
    filter_class = works_filters.IgualaFilter

    @transaction.atomic
    def create(self, request):
        """Overrided method because an Iguala has a list of Art types associated.
        All objects are sended directly in the same WS and here are processed.
        A roll back is done in case of failure so it's an atomic function
        """
        sid = transaction.savepoint()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_obj = self.obj_class.objects.create(**serializer.validated_data)
            art_igualas = request.data['art_iguala']
            for art_iguala in art_igualas:
                art_iguala['iguala'] = new_obj.id
                if not utils.save_object_from_data(models.ArtIguala,
                                                   serializers.ArtIgualaSerializer,
                                                   art_iguala):
                    transaction.savepoint_rollback(sid)
                    return utils.response_object_could_not_be_created(self.obj_class)

            return Response(self.serializer_class(new_obj).data, status=status.HTTP_201_CREATED)

        transaction.savepoint_rollback(sid)
        return utils.response_object_could_not_be_created(self.obj_class)

    def update(self, request, pk=None):
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            updated_obj = serializer.save()
            if 'art_iguala' not in request.data:
                return Response(self.serializer_class(updated_obj).data, status.HTTP_200_OK)
            art_igualas = request.data['art_iguala']
            for art_iguala in art_igualas:
                art_iguala['iguala'] = updated_obj.id
                art_type_id = art_iguala['art_type']
                try:
                    update_art_iguala_obj = models.ArtIguala.objects.get(iguala=updated_obj.id,
                                                                         art_type=art_type_id)
                except models.ArtIguala.DoesNotExist:
                    update_art_iguala_obj = None
                if update_art_iguala_obj is not None:
                    if not utils.update_object_from_data(serializers.ArtIgualaSerializer,
                                                         update_art_iguala_obj,
                                                         art_iguala):
                        return utils.response_object_could_not_be_created(self.obj_class)
                else:
                    if not utils.save_object_from_data(models.ArtIguala,
                                                       serializers.ArtIgualaSerializer,
                                                       art_iguala):
                        return utils.response_object_could_not_be_created(self.obj_class)

            return Response(self.serializer_class(updated_obj).data, status.HTTP_200_OK)

        return utils.response_object_could_not_be_created(self.obj_class)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)


class ArtIgualaViewSet(utils.GenericViewSet):
    """ViewSet for ArtIguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtIguala
    queryset = models.ArtIguala.objects.filter(is_active=True)
    serializer_class = serializers.ArtIgualaSerializer
    filter_class = works_filters.ArtIgualaFilter


class WorkViewSet(utils.GenericViewSet):
    """ViewSet for Work CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Work
    queryset = models.Work.objects.filter(is_active=True)
    serializer_class = serializers.WorkSerializer
    filter_class = works_filters.WorkFilter

    @detail_route(methods=['get'], url_path='possible-status-changes')
    def possible_status_changes(self, request, pk=None):
        queryset = models.Work.objects.filter(is_active=True)
        work = get_object_or_404(queryset, pk=pk)
        possible_status_changes = work.get_possible_status_changes(request.user)
        serializer = serializers.StatusSerializer(possible_status_changes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_obj = self.obj_class.objects.create(**serializer.validated_data)
            return Response(self.serializer_class(new_obj).data, status=status.HTTP_201_CREATED)

        return utils.response_object_could_not_be_created(self.obj_class)


class ArtWorkViewSet(utils.GenericViewSet):
    """ViewSet for ArtWork CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtWork
    queryset = models.ArtWork.objects.filter(is_active=True)
    serializer_class = serializers.ArtWorkSerializer
    filter_class = works_filters.ArtWorkFilter


class FileViewSet(utils.GenericViewSet):
    """ViewSet for File CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.File
    queryset = models.File.objects.filter(is_active=True)
    serializer_class = serializers.FileSerializer
    filter_class = works_filters.FileFilter


class WorkDesignerViewSet(utils.GenericViewSet):
    """ViewSet for WorkDesigner CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.WorkDesigner
    queryset = models.WorkDesigner.objects.filter(is_active=True)
    serializer_class = serializers.WorkDesignerSerializer
    filter_class = works_filters.WorkDesignerFilter


class StatusChangeViewSet(utils.GenericViewSet):
    """ViewSet for StatusChange CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.StatusChange
    queryset = models.StatusChange.objects.filter(is_active=True)
    serializer_class = serializers.StatusChangeSerializer
    filter_class = works_filters.StatusChangeFilter
