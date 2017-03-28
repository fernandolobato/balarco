from rest_framework import serializers
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',
                  'last_name', 'groups', )
        extra_kwargs = {
                        'username': {'required': True},
                        'password': {'required': False}
                        }
