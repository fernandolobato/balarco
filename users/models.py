from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to='media/profile_pictures')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_authentication_token(sender, instance=None, created=False, **kwargs):
    """ When a new user is created and saved, function
    creates a Token object for the created user """
    if created:
        Token.objects.create(user=instance)
