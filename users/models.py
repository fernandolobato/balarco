from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from channels import Group

from balarco import utils


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to='media/profile_pictures')


def save_profile(sender, instance, **kwargs):
    """Sends a notification to the user.
    """
    notification = {
        'notif_type': utils.NOTIF_TYPE_USERS_TABLE_CHANGE,
        'text': "Se ha actualizado la tabla de usuarios",
    }
    Group('users-table').send({
        'text': json.dumps(notification),
        })


post_save.connect(save_profile, sender=User)
