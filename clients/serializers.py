from rest_framework import serializers

from .models import Client, Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            'id',
            'is_active',
            'name',
            'last_name',
            'phone',
            'email',
            'alternate_email',
            'alternate_phone',
            'client'
        )


class ClientSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'address', 'contacts')
