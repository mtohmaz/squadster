
from rest_framework import serializers
from django.urls import reverse

from squadster.models import *

def datetime_serializer(obj):
    return obj.isoformat()

class SquadsterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SquadsterUser
        fields = '__all__'
        # need all read only?
        #read_only_fields = '__all__'
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)


class EventSerializer(serializers.ModelSerializer):
    """comments = serializers.HyperlinkedIdentityField(
        many=True,
        read_only=True,
        view_name='event-comment-list',
        lookup_field='parent_event',
        lookup_url_kwarg='event_id')
    """
    #comments = serializers.SerializerMethodField()
    
    #def get_comments(self, event):
    #    return reverse('event-comments', kwargs={'event_id':event.event_id})
    
    class Meta:
        model = Event
        fields = [
            'event_id',
            'host_id',
            'title',
            'date',
            'max_attendees',
            #'comments',
        ]
        read_only_fields = ['event_id']
    
    def create(self, validated_data):
        return Event.objects.create(**validated_data)

"""
class JoinedEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinedEvents
        fields = [
            'user_id',
            'event_id'
        ]
        
        read_only_fields = ['user_id', 'event_id']
"""        

class CommentSerializer(serializers.ModelSerializer):
    children = serializers.HyperlinkedIdentityField(
        many=True, read_only=True, view_name='event-comment-children-list')
    
    class Meta:
        model = Comment
        fields = [
            'comment_id',
            'parent_event',
            'author',
            'date_added',
            'text',
            'parent_comment',
            'children'
        ]
        
        read_only_fields = [
            'comment_id',
            'parent_event',
            'author',
            'date_added',
            'text', # allow editing the text in future? would also need date_edited
            'parent_comment'
        ]
    
