from django.contrib.auth.models import AbstractUser
from django.db import models

class twittaccess(models.Model):
	token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    user = models.ForeignKey( User )