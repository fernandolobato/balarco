from rest_framework import serializers
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.Serializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(serializers.Serializer):
    groups = GroupSerializer(many=True)
    username = serializers.EmailField()
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'groups',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        password = validated_data.get('password')
        return User.objects.create_user(
            username=username, first_name=first_name, last_name=last_name,
            email=email, password=password)
