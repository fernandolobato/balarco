"""Filter classes corresponding to each one of the works app's models that has the
same fields as the model for an equalTo filter.
There can be added extra fields inside each class as gt, lt, gte, lte and so on for
convinience.
"""

import django_filters
from django.contrib.auth.models import User, Group


class UserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class GroupFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = Group
        fields = ['id', 'name']
