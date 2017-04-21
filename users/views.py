from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers as serializers_library
from . import models, serializers
from . import filters as users_filters
from balarco import utils
from works.models import Work


class UserViewSet(utils.GenericViewSet):
    """ViewSet for User CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.User
    queryset = models.User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    filter_class = users_filters.UserFilter

    def create(self, request, pk=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            new_user = self.obj_class.objects.create_user(**serializer.validated_data)
            if 'groups_complete' not in request.data:
                return Response(self.serializer_class(new_user).data, status.HTTP_201_CREATED)
            groups = request.data['groups_complete']
            selected_groups = []
            for group in groups:
                group_id = group['id']
                current_group = Group.objects.get(id=group_id)
                current_group.user_set.add(new_user)
                selected_groups.append(group_id)
                current_group.save()
            unselected_groups = Group.objects.exclude(id__in=selected_groups)
            for group in unselected_groups:
                group.user_set.remove(new_user)
                group.save()
            return Response(self.serializer_class(new_user).data, status.HTTP_201_CREATED)
        else:
            return utils.response_object_could_not_be_created(self.obj_class)

    def update(self, request, pk=None):
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(obj, data=request.data)
        if serializer.is_valid():
            updated_user = serializer.save()
            if 'groups_complete' not in request.data:
                return Response(self.serializer_class(updated_user).data, status.HTTP_200_OK)
            groups = request.data['groups_complete']
            selected_groups = []
            for group in groups:
                group_id = group['id']
                current_group = Group.objects.get(id=group_id)
                current_group.user_set.add(updated_user)
                selected_groups.append(group_id)
                current_group.save()
            unselected_groups = Group.objects.exclude(id__in=selected_groups)
            for group in unselected_groups:
                group.user_set.remove(updated_user)
                group.save()
            return Response(self.serializer_class(updated_user).data, status.HTTP_200_OK)
        else:
            return utils.response_object_could_not_be_created(self.obj_class)

    def partial_update(self, request, pk=None):
        return self.update(request, pk)

    def destroy(self, request, pk=None):
        """Override of destroy method, with raises an exception when the selected
           user to delete belongs to a work object via executive relationship
        """
        queryset = self.obj_class.objects.filter(is_active=True)
        obj = get_object_or_404(queryset, pk=pk)
        works_queryset = Work.objects.filter(executive=obj)
        error_message = 'Antes de eliminar al usuario, reasigna todos sus proyectos'
        if works_queryset.count() > 0:
            raise serializers_library.ValidationError(error_message)
        else:
            obj.is_active = False
            try:
                obj.save()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status.HTTP_200_OK)
            except:
                raise Http404('No se pudo borrar el usuario en este momento')


class GroupViewSet(utils.GenericViewSet):
    """ViewSet for Group CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Group
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    filter_class = users_filters.GroupFilter
