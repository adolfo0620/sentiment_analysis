from django.db import models

<<<<<<< HEAD
class User(AbstractUser):
	pass


class Query(models.Model):
	created_at = models.DateField(auto_now_add=True)
	query_string = models.CharField (max_length=500)
	negative_score = models.IntegerField()
	positive_score = models.IntegerField()
	user = models.ForeignKey( "twitters.User" )
	media_platform = models.CharField(max_length=250)
=======
## django does not like this...
# class User(AbstractUser):
#     pass
>>>>>>> 1d741b41dcf70b0bbedb5049485716e2125b2646
