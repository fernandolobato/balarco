"""Filter classes corresponding to each one of the clients app's models that has the
same fields as the model for an equalTo filter.
There can be added extra fields inside each class as gt, lt, gte, lte and so on for
convinience.
"""

import django_filters
from . import models as client_models


class ClientFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = client_models.Client
        fields = ['id', 'name', 'address']


class ContactFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = client_models.Contact
        fields = ['id', 'client', 'name', 'last_name', 'charge', 'landline', 'extension',
                  'mobile_phone_1', 'mobile_phone_2', 'email', 'alternate_email']
