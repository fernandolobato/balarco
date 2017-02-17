from django.conf.urls import url
from rest_framework.authtoken import views as authviews
from . import views

app_name = 'users'

urlpatterns = [
	url(r'^api-login/', authviews.obtain_auth_token, name='api_login'),
]