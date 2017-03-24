import django_filters
from . import models as works_models


class WorkTypeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.WorkType
        fields = ['id', 'work_type_id', 'name']


class ArtTypeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.ArtType
        fields = ['id', 'work_type', 'name']


class IgualaFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.Iguala
        fields = ['id', 'client', 'name', 'start_date', 'end_date']


class ArtIgualaFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.ArtIguala
        fields = ['id', 'iguala', 'art_type', 'quantity']


class WorkFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.Work
        fields = ['id', 'executive', 'contact', 'current_status', 'work_type', 'iguala',
                  'creation_date', 'name', 'expected_delivery_date', 'brief', 'final_link']


class ArtWorkFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.ArtWork
        fields = ['id', 'work', 'art_type', 'quantity']


class FileFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.File
        fields = ['id', 'work']


class WorkDesignerFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.WorkDesigner
        fields = ['id', 'designer', 'work', 'start_date', 'end_date', 'active_work']


class StatusChangeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.StatusChange
        fields = ['id', 'work', 'status', 'user', 'date']
