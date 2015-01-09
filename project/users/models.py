from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass


class Query(models.Model):
	created_at = models.DateField(auto_now_add=True)
	query_string = models.CharField (max_length=500)
	negative_score = models.IntegerField()
	positive_score = models.IntegerField()
	user = models.ForeignKey( "twitters.User" )
	media_platform = models.CharField(max_length=250)