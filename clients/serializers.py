from rest_framework import serializers

from .models import Client, Contact


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'address',)


class ContactSerializer(serializers.ModelSerializer):

    client_complete = ClientSerializer(source='client', read_only=True)

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
            'client',
            'client_complete',
        )
