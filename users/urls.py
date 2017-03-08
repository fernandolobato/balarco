from django.conf.urls import url
from rest_framework.authtoken import views as authviews
import djoser.views

app_name = 'users'

urlpatterns = [
    url(r'^auth/login/', authviews.obtain_auth_token, name='api_login'),
    url(r'^auth/register/', djoser.views.RegistrationView.as_view(), name='api_registration'),
    url(r'^auth/password/reset/', djoser.views.PasswordResetView.as_view(),
        name='api_reset_password'),
    url(r'^auth/password/reset/confirm/', djoser.views.PasswordResetConfirmView.as_view()),
]
