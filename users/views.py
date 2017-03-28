from django.contrib.auth.models import Group
from . import models, serializers
from balarco import utils


class UserViewSet(utils.GenericViewSet):
    """ViewSet for User CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.User
    queryset = models.User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer


class GroupViewSet(utils.GenericViewSet):
    """ViewSet for Group CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = Group
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
