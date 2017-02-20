from rest_framework import serializers
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.Serializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups',)
        extra_kwargs = {'password': {'write_only': True}}
