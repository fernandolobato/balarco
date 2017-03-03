from rest_framework import serializers

from . import models


class WorkTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkType
        fields = ('id', 'name', 'is_active')


class ArtypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtType
        fields = ('id', 'work_type', 'name', 'is_active')


class IgualaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Iguala
        fields = ('id', 'client', 'name', 'start_date', 'end_date', 'is_active')


class ArtIgualaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtIguala
        fields = ('id', 'iguala', 'art_type', 'quantity', 'is_active')


class WorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Work
        fields = ('id',
                  'executive',
                  'contact',
                  'current_status',
                  'work_type',
                  'iguala',
                  'creation_date',
                  'name',
                  'expected_delivery_date',
                  'brief',
                  'final_link',
                  'is_active')


class ArtWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ArtWork
        fields = ('id', 'work', 'art_type', 'quantity', 'is_active')


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.File
        fields = ('id', 'work', 'upload', 'is_active')


class WorkDesignerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WorkDesigner
        fields = ('id', 'designer', 'work', 'start_date', 'end_date', 'is_active')


class StatusChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StatusChange
        fields = ('id', 'work', 'status', 'user', 'date', 'is_active')
