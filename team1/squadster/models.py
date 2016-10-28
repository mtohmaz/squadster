from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



"""
from oauth2client.contrib.django_orm import FlowField
from oauth2client.contrib.django_orm import CredentialsField


class CredentialsModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  credential = CredentialsField()

class FlowModel(models.Model):
  id = models.ForeignKey(User, primary_key=True)
  flow = FlowField()
"""


# User handling

class SquadsterUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name = 'profile')
    #enabled = models.BooleanField(default=True)
    api_key_last_auth = models.DateTimeField(default=None, null=True)
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []
    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, **kwargs):
        if created:
            SquadsterUser.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user(sender, instance, **kwargs):
        instance.profile.save()


class Moderator(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.DO_NOTHING, primary_key=True)
    
    #automatically add the timestamp
    date_added = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.DO_NOTHING, primary_key=True)
    
    #automatically add the timestamp
    date_added = models.DateTimeField(auto_now_add=True)


# Event handling
# TODO location postgres
class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='hostedevents')
    attendees = models.ManyToManyField(User, related_name='joinedevents')
    title = models.CharField(max_length=64)
    date = models.DateTimeField()
    max_attendees = models.IntegerField()
    description = models.CharField(max_length=250)

#class JoinedEvents(models.Model):
#    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='joinedevents')
#    event_id = models.ForeignKey('Event', on_delete=models.DO_NOTHING, related_name='attendees')

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    parent_event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250)
    moderated = models.BooleanField(default=False)
    parent_comment = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='children')


# Report handling
class ReportedUsers(models.Model):
    incident_id = models.AutoField(primary_key=True)
    reported_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_id')
    reported_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reported_by')
    moderated_by = models.ForeignKey('Moderator', on_delete=models.DO_NOTHING)
    disabled_by = models.ForeignKey('Admin', on_delete=models.DO_NOTHING)
    time_reported = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField()
    time_disabled = models.DateTimeField()

class ReportedEvents(models.Model):
    incident_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)
    reported_by = models.ForeignKey('SquadsterUser', on_delete=models.DO_NOTHING)
    moderated_by = models.ForeignKey('Moderator', on_delete=models.DO_NOTHING)
    time_reported = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField()

class ReportedComments(models.Model):
    incident_id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    reported_by = models.ForeignKey('SquadsterUser', on_delete=models.DO_NOTHING)
    moderated_by = models.ForeignKey('Moderator', on_delete=models.DO_NOTHING)
    time_reported = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField()


# Tag handling
class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=64)

class EventTags(models.Model):
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)
    tag_id = models.ForeignKey('Tags', on_delete=models.CASCADE)
    
    
