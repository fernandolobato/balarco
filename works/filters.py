"""Filter classes corresponding to each one of the works app's models that has the
same fields as the model for an equalTo filter.
There can be added extra fields inside each class as gt, lt, gte, lte and so on for
convinience.
"""

import django_filters
from . import models as works_models


class WorkTypeFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.WorkType
        fields = ['id', 'work_type_id', 'name']


class ArtTypeFilter(django_filters.rest_framework.FilterSet):

    work_work_type_id = django_filters.NumberFilter(name='work_type__work_type_id')

    class Meta:
        model = works_models.ArtType
        fields = ['id', 'work_type', 'name', 'work_work_type_id']


class IgualaFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.Iguala
        fields = ['id', 'client', 'name', 'start_date', 'end_date']


class ArtIgualaFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.ArtIguala
        fields = ['id', 'iguala', 'art_type', 'quantity']


class StatusFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = works_models.Status
        fields = ['id', 'status_id']


class WorkFilter(django_filters.rest_framework.FilterSet):

    creation_date_min = django_filters.DateFilter(name='creation_date', lookup_expr='gte')
    creation_date_max = django_filters.DateFilter(name='creation_date', lookup_expr='lte')
    expected_delivery_date_min = django_filters.DateFilter(name='expected_delivery_date',
                                                           lookup_expr='gte')
    expected_delivery_date_max = django_filters.DateFilter(name='expected_delivery_date',
                                                           lookup_expr='lte')

    class Meta:
        model = works_models.Work
        fields = ['id', 'executive', 'contact', 'current_status', 'work_type', 'iguala',
                  'creation_date', 'name', 'expected_delivery_date', 'brief', 'final_link',
                  'creation_date_min', 'creation_date_max', 'expected_delivery_date_min',
                  'expected_delivery_date_max']


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
