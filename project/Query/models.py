from django.db import models
from django.contrib.auth.models import User

class Query(models.Model):
	created_at = models.DateField(auto_now_add=True)
	query_string = models.CharField (max_length=500)
	negative_score = models.IntegerField()
	positive_score = models.IntegerField()
	user = models.ForeignKey( User )
	media_platform = models.CharField(max_length=250)