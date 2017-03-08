from rest_framework import serializers
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.Serializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.Serializer):
    groups = GroupSerializer(many=True, required=False)
    username = serializers.EmailField(allow_blank=False)
    first_name = serializers.CharField(max_length=200, allow_blank=False)
    last_name = serializers.CharField(max_length=200, allow_blank=False)
    email = serializers.EmailField(allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'}, allow_blank=False)

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        return User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name,
            email=email, password=password)
