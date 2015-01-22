from django.db import models
from django.contrib.auth.models import User

class Twitter_access(models.Model):
    token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    user = models.ForeignKey( User )
