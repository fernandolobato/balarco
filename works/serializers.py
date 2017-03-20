from rest_framework import serializers

from . import models
from clients import serializers as client_serializers
from users import serializers as user_serializers


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkType
        fields = ('id', 'name',)


class ArtTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtType
        fields = ('id', 'work_type', 'name',)


class ArtIgualaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtIguala
        fields = ('id', 'art_type', 'quantity',)


class IgualaSerializer(serializers.ModelSerializer):

    client_complete = client_serializers.ClientSerializer(source='client', read_only=True)
    art_iguala = ArtIgualaSerializer(many=True, read_only=True)

    class Meta:
        model = models.Iguala
        fields = ('id', 'client', 'client_complete', 'name', 'start_date', 'end_date',
                  'art_iguala',)


class StatusSerializer(serializers.ModelSerializer):

    name = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = models.Status
        fields = ('id', 'status_id', 'name',)


class WorkSerializer(serializers.ModelSerializer):

    creation_date = serializers.DateField(read_only=True)
    executive_complete = user_serializers.UserSerializer(source='executive', read_only=True)
    contact_complete = client_serializers.ContactSerializer(source='contact', read_only=True)
    current_status_complete = StatusSerializer(source='current_status', read_only=True)
    work_type_complete = WorkTypeSerializer(source='work_type', read_only=True)
    iguala_complete = IgualaSerializer(source='iguala', read_only=True)

    class Meta:
        model = models.Work
        fields = ('id',
                  'executive',
                  'executive_complete',
                  'contact',
                  'contact_complete',
                  'current_status',
                  'current_status_complete',
                  'work_type',
                  'work_type_complete',
                  'iguala',
                  'iguala_complete',
                  'creation_date',
                  'name',
                  'expected_delivery_date',
                  'brief',
                  'final_link',
                  )


class ArtWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtWork
        fields = ('id', 'work', 'art_type', 'quantity',)


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.File
        fields = ('id', 'work', 'upload',)


class WorkDesignerSerializer(serializers.ModelSerializer):

    start_date = serializers.DateTimeField(read_only=True)
    end_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.WorkDesigner
        fields = ('id', 'designer', 'work', 'start_date', 'end_date', 'active_work',)


class StatusChangeSerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.StatusChange
        fields = ('id', 'work', 'status', 'user', 'date',)
