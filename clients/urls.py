from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = 'clients'

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet, base_name='Clients')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-contact/(?P<contact>[0-9]+)', views.APIContact.as_view(),
        name='api_contact_detail'),
    url(r'^api-contact', views.APIContact.as_view(), name='api_contact'),
]
