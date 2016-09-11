from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=64)
	user_id = models.CharField(max_length=200, primary_key=True)
	permission_level = models.IntegerField(default=0)
	enabled = models.BooleanField(default=True)

class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	title = models.CharField(max_length=64)
	description = models.CharField(max_length=250)
	host_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	enabled = models.BooleanField(default=True)

class User_Event(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	event_id = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

class Comment(models.Model):
	event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
	text = models.CharField(max_length=250)
