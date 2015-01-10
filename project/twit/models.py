from django.db import models

<<<<<<< HEAD
class Twitter_access(models.Model):
    token = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    user = models.ForeignKey( "twitters.User" )
=======

# class User():
	
>>>>>>> 1d741b41dcf70b0bbedb5049485716e2125b2646
