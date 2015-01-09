from django.contrib.auth.models import AbstractUser
from django.db import models

class Twitter_access(models.Model):
    token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    user = models.ForeignKey( "twitters.User" )