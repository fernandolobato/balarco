from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


def generic_rest_list_objects(request, serializer_class, obj_class):
    """
    Function to list all objects of a model in GenericViewSet:list.
    It makes a Query to the specified object class geting all active objects
    """
    queryset = obj_class.objects.filter(is_active=True)
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


def generic_rest_create_object(request, serializer_class, obj_class):
    """
    Function used in GenericViewSet:create to create and save a
    new object of the specified class.
    """
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        new_obj = obj_class.objects.create(**serializer.validated_data)
        return Response(serializer_class(new_obj).data, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be created with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_retrieve_object(request, serializer_class, obj_class, pk):
    """
    Function used by GenericViewSet:retrieve to retrieve the data of specified object.
    The object must be active to get it.
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj)
    return Response(serializer.data, status.HTTP_200_OK)


def generic_rest_update_object(request, serializer_class, obj_class, pk, partial_update):
    """
    Function used by GenericViewSet:update and GenericViewSet:partial_update to edit
    the data of the specified object.
    It receives a boolean called partial_update depending on which type of request is being
    handled (PUT/PATCH).
    The object must be active to edit it.
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj, data=request.data, partial=partial_update)
    if serializer.is_valid():
        updated_obj = serializer.save()
        return Response(serializer_class(updated_obj).data, status.HTTP_200_OK)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be updated with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_soft_delete(request, serializer_class, obj_class, pk):
    """
    Function used by GenericViewSet:destroy to make a soft delete of the specified object.
    This means that the object is not truly deleted but its active state change to false.
    The object must be active to delete it.
    """
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    obj.is_active = False
    obj.save()
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data, status.HTTP_200_OK)


class GenericViewSet(viewsets.ViewSet):
    """
    Generic view set for basic CRUD REST Service.

    To use it a ViewSet has to inherit from it and add the attributes:
    obj_class: The model class
        Class of the main model that the REST is going to work on
    serializer_class: The serializer class of the model
        Class of the serializer that is going to represent the obj_class
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    obj_class = None
    serializer_class = None

    def list(self, request):
        return generic_rest_list_objects(request, self.serializer_class, self.obj_class)

    def create(self, request):
        return generic_rest_create_object(request, self.serializer_class, self.obj_class)

    def retrieve(self, request, pk=None):
        return generic_rest_retrieve_object(request, self.serializer_class, self.obj_class, pk)

    def update(self, request, pk=None):
        return generic_rest_update_object(request, self.serializer_class,
                                          self.obj_class, pk, False)

    def partial_update(self, request, pk=None):
        return generic_rest_update_object(request, self.serializer_class, self.obj_class, pk, True)

    def destroy(self, request, pk=None):
        return generic_rest_soft_delete(request, self.serializer_class, self.obj_class, pk)
