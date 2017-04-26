import json

from django.db import models
from channels import Group

from balarco import utils


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        """
        Override of save function.
        If the is_active field is false, it means that the object was deleted so it starts
        a CASCADE soft deletion over all model dependencies.
        """
        if not self.is_active:
            queryset = Contact.objects.filter(client=self)
            for contact in queryset:
                contact.is_active = False
                contact.save()
        super(Client, self).save(*args, **kwargs)
        """Sends a notification to the user.
        """
        notification = {
            'notif_type': utils.NOTIF_TYPE_CLIENTS_TABLE_CHANGE,
            'text': "Se ha actualizado la tabla de clientes",
        }
        Group('clients-table').send({
            'text': json.dumps(notification),
            })


class Contact(models.Model):
    client = models.ForeignKey(Client, related_name='contacts', on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    charge = models.CharField(max_length=255)
    landline = models.CharField(max_length=50)
    extension = models.CharField(max_length=50, blank=True)
    mobile_phone_1 = models.CharField(max_length=50)
    mobile_phone_2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255)
    alternate_email = models.EmailField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.last_name)
