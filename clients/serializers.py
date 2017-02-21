from rest_framework import serializers

from clients.models import Client, Contact


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

    def create(self, validated_data):
        if 'id' in self.context['request'].data:
            pk = self.context['request'].data['id']
            Contact.objects.filter(id=pk).update(**validated_data)
            contact = Contact.objects.get(id=pk)
        else:
            contact = Contact.objects.create(**validated_data)
            contact.save()
        return contact


class ClientSerializer(serializers.ModelSerializer):

    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ('id', 'name', 'address', 'contacts')
