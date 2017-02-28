from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = 'clients'

router = routers.DefaultRouter()
router.register(r'clients', views.ClientViewSet, base_name='clients')
router.register(r'contacts', views.ContactViewSet, base_name='contacts')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
