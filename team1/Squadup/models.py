from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=58)
	


class Event(models.Model):
	title = models.CharField(max_length=58)
