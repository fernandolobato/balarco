from django.conf.urls import url

from . import views

app_name = 'users'

urlpatterns = [
	url(r'^api-login$', views.APILogin.as_view(), name='api_login'),
]