import csv

from rest_framework.decorators import detail_route, list_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers as serializers_library
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.http import Http404

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

    def destroy(self, request, pk=None):
        """Override of destroy method, with raises an exception when the selected
           user to delete belongs to a work object via iguala relationship
        """
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        work_queryset = models.Work.objects.filter(iguala=obj)
        error_message = 'Antes de eliminar la iguala, reasigna todos los proyectos'
        if work_queryset.count() > 0:
            raise serializers_library.ValidationError(error_message)
        else:
            obj.is_active = False
            try:
                obj.save()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            except:
                return Http404('No se pudo borrar la iguala en este momento')

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
            if 'art_iguala' in request.data:
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

    @transaction.atomic
    def update(self, request, pk=None):
        sid = transaction.savepoint()
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            updated_obj = serializer.save()
            if 'art_iguala' in request.data:
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
                            transaction.savepoint_rollback(sid)
                            return utils.response_object_could_not_be_created(self.obj_class)
                    else:
                        if not utils.save_object_from_data(models.ArtIguala,
                                                           serializers.ArtIgualaSerializer,
                                                           art_iguala):
                            transaction.savepoint_rollback(sid)
                            return utils.response_object_could_not_be_created(self.obj_class)

            return Response(self.serializer_class(updated_obj).data, status.HTTP_200_OK)

        transaction.savepoint_rollback(sid)
        return utils.response_object_could_not_be_created(self.obj_class)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    @detail_route(methods=['get'], url_path='report')
    def report(self, request, pk=None):
        queryset = models.Iguala.objects.filter(is_active=True)
        iguala = get_object_or_404(queryset, pk=pk)
        response = HttpResponse(content_type='text/csv')
        str_now = timezone.now().strftime('%d-%m-%Y %H-%M')
        response['Content-Disposition'] = 'attachment; filename="{}-{}.csv"'.format(iguala.name,
                                                                                    str_now)

        works = models.Work.objects.filter(is_active=True, iguala=iguala)
        writer = csv.writer(response)

        writer.writerow([iguala.name, timezone.now().strftime('%d-%m-%Y %H:%M')])
        writer.writerow([])
        writer.writerow([])

        art_works_count = {}
        for work in works:
            for art_work in work.art_works.all():
                art_type_id = art_work.art_type.id
                if art_type_id in art_works_count:
                    art_works_count[art_type_id] += art_work.quantity
                else:
                    art_works_count[art_type_id] = art_work.quantity

        writer.writerow(['Tipo de arte', 'Contratadas', 'Usadas', 'Restantes'])

        for art_iguala in iguala.art_iguala.all():
            art_type_id = art_iguala.art_type.id
            art_type_name = art_iguala.art_type.name
            agreed = art_iguala.quantity
            if art_type_id in art_works_count:
                used = art_works_count[art_type_id]
                remaining = agreed - used
                writer.writerow([art_type_name, agreed, used, remaining])
            else:
                used = 0
                remaining = agreed - used
                writer.writerow([art_type_name, agreed, used, remaining])

        writer.writerow([])
        writer.writerow([])
        writer.writerow(['Trabajos relacionados con la iguala'])

        for work in works:
            writer.writerow([])
            writer.writerow([])
            writer.writerow(['Trabajo', 'Contacto', 'Empresa', 'Fecha entrada', 'Status actual'])
            work_name = work.name
            contact_name = '{} {}'.format(work.contact.name, work.contact.last_name)
            client_name = work.contact.client.name
            creation_date = work.creation_date.strftime('%d-%m-%Y')
            current_status = work.current_status.__str__()
            writer.writerow([work_name, contact_name, client_name, creation_date, current_status])
            writer.writerow([])
            writer.writerow(['', 'Tipo de arte', 'Cantidad'])
            for art_work in work.art_works.all():
                art_type_name = art_work.art_type.name
                quantity = art_work.quantity
                writer.writerow(['', art_type_name, quantity])

        return response


class ArtIgualaViewSet(utils.GenericViewSet):
    """ViewSet for ArtIguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtIguala
    queryset = models.ArtIguala.objects.filter(is_active=True)
    serializer_class = serializers.ArtIgualaSerializer
    filter_class = works_filters.ArtIgualaFilter


class StatusViewSet(utils.GenericViewSet):
    """ViewSet for Status CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Status
    queryset = models.Status.objects.filter(is_active=True)
    serializer_class = serializers.StatusSerializer
    filter_class = works_filters.StatusFilter


class WorkViewSet(utils.GenericViewSet):
    """ViewSet for Work CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Work
    queryset = models.Work.objects.filter(is_active=True)
    serializer_class = serializers.WorkSerializer
    filter_class = works_filters.WorkFilter

    @list_route(methods=['get'], url_path='my_assignments')
    def my_assignments(self, request):
        user = request.user
        asigned_works = user.asigned_works.filter(active_work=True)
        works = set()
        for asigned_work in asigned_works:
            works.add(asigned_work.work)
        serializer = serializers.WorkSerializer(works, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @list_route(methods=['get'], url_path='unassigned_works')
    def unassigned_works(self, request):
        works = models.Work.objects.filter(is_active=True)
        unassigned_works = set()
        for work in works:
            work_designers = work.work_designers.filter(active_work=True)
            current_status_id = work.current_status.status_id
            if current_status_id == models.Status.STATUS_DISENO and len(work_designers) == 0:
                unassigned_works.add(work)
        serializer = serializers.WorkSerializer(unassigned_works, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @detail_route(methods=['get'], url_path='possible-status-changes')
    def possible_status_changes(self, request, pk=None):
        queryset = models.Work.objects.filter(is_active=True)
        work = get_object_or_404(queryset, pk=pk)
        possible_status_changes = work.get_possible_status_changes(request.user)
        serializer = serializers.StatusSerializer(possible_status_changes, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def create(self, request):
        sid = transaction.savepoint()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_obj = self.obj_class.objects.create(**serializer.validated_data)
            if 'art_works' in request.data:
                art_works = request.data['art_works']
                for art_work in art_works:
                    art_work['work'] = new_obj.id
                    if not utils.save_object_from_data(models.ArtWork,
                                                       serializers.ArtWorkSerializer,
                                                       art_work):
                        transaction.savepoint_rollback(sid)
                        return utils.response_object_could_not_be_created(self.obj_class)

            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
                models.File.objects.create(work=new_obj, filename=name, upload=file)

            if 'work_designers' in request.data:
                work_designers = request.data['work_designers']
                for work_designer in work_designers:
                    work_designer['work'] = new_obj.id
                    if not utils.save_object_from_data(models.WorkDesigner,
                                                       serializers.WorkDesignerSerializer,
                                                       work_designer):
                        transaction.savepoint_rollback(sid)
                        return utils.response_object_could_not_be_created(self.obj_class)

            models.StatusChange.objects.create(work=new_obj, status=new_obj.current_status,
                                               user=request.user)

            return Response(self.serializer_class(new_obj).data, status=status.HTTP_201_CREATED)

        return utils.response_object_could_not_be_created(self.obj_class)

    def update(self, request, pk=None):
        sid = transaction.savepoint()
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data, partial=True)
        if serializer.is_valid():
            status_has_changed = False
            if 'current_status' in request.data:
                status_has_changed = request.data['current_status'] != obj.current_status.id
            updated_obj = serializer.save()
            if 'art_works' in request.data:
                art_works = request.data['art_works']
                for art_work in art_works:
                    art_work['work'] = updated_obj.id
                    art_type_id = art_work['art_type']
                    try:
                        update_art_work_obj = models.ArtWork.objects.get(work=updated_obj.id,
                                                                         art_type=art_type_id)
                    except models.ArtWork.DoesNotExist:
                        update_art_work_obj = None
                    if update_art_work_obj is not None:
                        if not utils.update_object_from_data(serializers.ArtWorkSerializer,
                                                             update_art_work_obj,
                                                             art_work):
                            transaction.savepoint_rollback(sid)
                            return utils.response_object_could_not_be_created(self.obj_class)
                    else:
                        if not utils.save_object_from_data(models.ArtWork,
                                                           serializers.ArtWorkSerializer,
                                                           art_work):
                            transaction.savepoint_rollback(sid)
                            return utils.response_object_could_not_be_created(self.obj_class)

            for filename, file in request.FILES.items():
                name = request.FILES[filename].name
                models.File.objects.create(work=updated_obj, filename=name, upload=file)

            if 'work_designers' in request.data:
                work_designers = request.data['work_designers']
                for work_designer in work_designers:
                    work_designer['work'] = updated_obj.id
                    designer_id = work_designer['designer']
                    active_work = work_designer['active_work']
                    try:
                        update_work_designer = \
                            models.WorkDesigner.objects.get(work=updated_obj.id,
                                                            designer=designer_id,
                                                            active_work=True)
                    except models.WorkDesigner.DoesNotExist:
                        update_work_designer = None

                    if update_work_designer is not None:
                        if not utils.update_object_from_data(serializers.WorkDesignerSerializer,
                                                             update_work_designer,
                                                             work_designer):
                            transaction.savepoint_rollback(sid)
                            return utils.response_object_could_not_be_created(self.obj_class)
                    else:
                        if active_work:
                            if not utils.save_object_from_data(models.WorkDesigner,
                                                               serializers.WorkDesignerSerializer,
                                                               work_designer):
                                transaction.savepoint_rollback(sid)
                                return utils.response_object_could_not_be_created(self.obj_class)

            if status_has_changed:
                models.StatusChange.objects.create(work=updated_obj,
                                                   status=updated_obj.current_status,
                                                   user=request.user)

            return Response(self.serializer_class(updated_obj).data, status.HTTP_200_OK)

        return utils.response_object_could_not_be_created(self.obj_class)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)


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


class NotificationViewSet(utils.GenericViewSet):
    """ViewSet for Notification CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Notification
    queryset = models.Notification.objects.filter(is_active=True)
    serializer_class = serializers.NotificationSerializer
    filter_class = works_filters.NotificationFilter

    @list_route(methods=['get'], url_path='read_all')
    def read_all(self, request):
        user = request.user
        unseen_notifications = models.Notification.objects.filter(user=user, seen=False)
        for notification in unseen_notifications:
            notification.seen = True
            notification.save()
        return self.unseen_notifications(request)

    @list_route(methods=['get'], url_path='unseen_notifications')
    def unseen_notifications(self, request):
        user = request.user
        queryset = models.Notification.objects.filter(is_active=True, user=user, seen=False)
        serializer = serializers.NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
