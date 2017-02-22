from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


def generic_rest_list_objects(request, serializer_class, obj_class):
    queryset = obj_class.objects.filter(is_active=True)
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)


def generic_rest_create_object(request, serializer_class, obj_class):
    serializer = serializer_class(data=request.data)
    if serializer.is_valid():
        new_obj = obj_class.objects.create(**serializer.validated_data)
        print(serializer.validated_data)
        return Response(serializer_class(new_obj).data, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be created with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_retrieve_object(request, serializer_class, obj_class, pk):
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj)
    return Response(serializer.data)


def generic_rest_update_object(request, serializer_class, obj_class, pk, partial_update):
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    serializer = serializer_class(obj, data=request.data, partial=partial_update)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({
        'status': 'Bad request',
        'message': '%s could not be updated with received data.' % obj_class.__name__
    }, status=status.HTTP_400_BAD_REQUEST)


def generic_rest_soft_delete(request, serializer_class, obj_class, pk):
    queryset = obj_class.objects.filter(is_active=True)
    obj = get_object_or_404(queryset, pk=pk)
    obj.is_active = False
    obj.save()
    serializer = serializer_class(queryset, many=True)
    return Response(serializer.data)


class GenericViewSet(viewsets.ViewSet):
    """
    Generic view set for basic CRUD REST Service.

    To use it a ViewSet has to inherit from it and add the attributes:
    -obj_class: The model class
    -serializer_class: The serializer class of the model
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
