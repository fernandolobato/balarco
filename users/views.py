from . import models, serializers
from balarco import utils


class UserViewSet(utils.GenericViewSet):
    """ViewSet for User CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.User
    queryset = models.User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
