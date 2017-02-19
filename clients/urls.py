from django.conf.urls import url

from . import views

app_name = 'clients'

urlpatterns = [
	url(r'^api-contact/(?P<contact>[0-9]+)', views.APIContact.as_view(), name='api_contact_detail'),
	url(r'^api-contact', views.APIContact.as_view(), name='api_contact'),
]
