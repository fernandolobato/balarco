from . import models, serializers
from balarco import utils


class WorkTypeViewSet(utils.GenericViewSet):
    """ViewSet for WorkType CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.WorkType
    serializer_class = serializers.WorkTypeSerializer


class ArtTypeViewSet(utils.GenericViewSet):
    """ViewSet for ArtType CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtType
    serializer_class = serializers.ArtTypeSerializer


class IgualaViewSet(utils.GenericViewSet):
    """ViewSet for Iguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Iguala
    serializer_class = serializers.IgualaSerializer


class ArtIgualaViewSet(utils.GenericViewSet):
    """ViewSet for ArtIguala CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtIguala
    serializer_class = serializers.ArtIgualaSerializer


class WorkViewSet(utils.GenericViewSet):
    """ViewSet for Work CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.Work
    serializer_class = serializers.WorkSerializer


class ArtWorkViewSet(utils.GenericViewSet):
    """ViewSet for ArtWork CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.ArtWork
    serializer_class = serializers.ArtWorkSerializer


class FileViewSet(utils.GenericViewSet):
    """ViewSet for File CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.File
    serializer_class = serializers.FileSerializer


class WorkDesignerViewSet(utils.GenericViewSet):
    """ViewSet for WorkDesigner CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.WorkDesigner
    serializer_class = serializers.WorkDesignerSerializer


class StatusChangeViewSet(utils.GenericViewSet):
    """ViewSet for StatusChange CRUD REST Service that inherits from utils.GenericViewSet
    """
    obj_class = models.StatusChange
    serializer_class = serializers.StatusChangeSerializer
