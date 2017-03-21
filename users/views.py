from rest_framework.decorators import detail_route
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers
from balarco import utils


class UserViewSet(utils.GenericViewSet):
    """ViewSet for User CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.User
    queryset = models.User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer