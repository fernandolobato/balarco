from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	profile_picture = models.ImageField(upload_to='media/profile_pictures')
