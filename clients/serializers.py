from rest_framework import serializers

from .models import Client, Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'last_name',
            'charge',
            'landline',
            'extension',
            'mobile_phone_1',
            'mobile_phone_2',
            'email',
            'alternate_email',
            'is_active',
            'client'
        )


class ClientSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'address', 'contacts')
