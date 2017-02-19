from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Contact(models.Model):
	client = models.ForeignKey('Client')

	name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	alternate_email = models.EmailField(max_length=255, blank=True)
	phone = models.CharField(max_length=50, blank=True)
	alternate_phone = models.CharField(max_length=50, blank=True)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return '%s %s' % (self.name, self.last_name)
