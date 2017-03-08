from django.conf.urls import url
from rest_framework.authtoken import views as authviews
import djoser.views

app_name = 'users'

urlpatterns = [
    #url(r'^api-login/', authviews.obtain_auth_token, name='api_login'),
    # url(r'^auth/login', rest_framework_jwt.views.obtain_jwt_token),  # using JSON web token
    url(r'^auth/login/', authviews.obtain_auth_token, name='api_login'),
    url(r'^auth/register', djoser.views.RegistrationView.as_view()),
    url(r'^auth/password/reset', djoser.views.PasswordResetView.as_view()),
    url(r'^auth/password/reset/confirm', djoser.views.PasswordResetConfirmView.as_view()),
]
