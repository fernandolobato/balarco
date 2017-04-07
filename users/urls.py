from django.conf.urls import url, include
from rest_framework.authtoken import views as authviews
from rest_framework import routers
import djoser.views

from . import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, base_name='users')
router.register(r'groups', views.GroupViewSet, base_name='groups')

urlpatterns = [
    url(r'^auth/login/', authviews.obtain_auth_token, name='api_login'),
    url(r'^auth/register/', djoser.views.RegistrationView.as_view(), name='api_registration'),
    url(r'^auth/password/reset/$', djoser.views.PasswordResetView.as_view(),
        name='api_reset_password'),
    url(r'^auth/password/reset/confirm/', djoser.views.PasswordResetConfirmView.as_view(),
        name='api_reset_password_confirm'),
    url(r'^', include(router.urls)),
]
