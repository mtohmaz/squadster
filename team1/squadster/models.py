from django.db import models
"""
class User(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    token = models.CharField(max_length=1000)
    enabled = models.BooleanField(default=True)
"""
class Moderator(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, primary_key=True)
    #automatically add the timestamp
    date_added = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE, primary_key=True)
    #automatically add the timestamp
    date_added = models.DateTimeField(auto_now_add=True)

class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    host_id = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)

class JoinedEvents(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    event_id = models.ForeignKey('Event', on_delete=models.DO_NOTHING)

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    parent_event = models.ForeignKey('Event', on_delete=models.CASCADE)
    author = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    date_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=250)
    moderated = models.BooleanField(default=False)


# Report handling
class ReportedUsers(models.Model):
    incident_id = models.AutoField(primary_key=True)
    reported_id = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reported_id')
    reported_by = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='reported_by')
    moderated_by = models.ForeignKey('Moderator', on_delete=models.DO_NOTHING)
    disabled_by = models.ForeignKey('Admin', on_delete=models.DO_NOTHING)
    time_reported = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField()
    time_disabled = models.DateTimeField()

class ReportedEvents(models.Model):
    incident_id = models.AutoField(primary_key=True)
    event_id = models.ForeignKey('Event', on_delete=models.CASCADE)
    reported_by = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    moderated_by = models.ForeignKey('Moderator', on_delete=models.DO_NOTHING)
    time_reported = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField()

class ReportedComments(models.Model):
    incident_id = models.AutoField(primary_key=True)
    comment_id = models.ForeignKey('Comment', on_delete=models.CASCADE)
    reported_by = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    moderated_by = models.ForeignKey('Moderator', on_delete=models.DO_NOTHING)
    time_reported = models.DateTimeField(auto_now_add=True)
    time_moderated = models.DateTimeField()
