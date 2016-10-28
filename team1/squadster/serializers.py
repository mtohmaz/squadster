
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
    comments = serializers.SerializerMethodField()
    summary_fields = serializers.SerializerMethodField()
    
    def get_comments(self, event):
        request = self.context.get('request')
        return request.build_absolute_uri(
                reverse('event-comment-list', kwargs={'event_id':event.event_id}))
    
    def get_summary_fields(self, obj):
        return {
            'number_of_children': Comment.objects.filter(parent_event=obj.event_id).count()
        
        }
    
    class Meta:
        model = Event
        fields = [
            'event_id',
            'host_id',
            'title',
            'date',
            'max_attendees',
            'comments',
            'summary_fields'
        ]
        read_only_fields = ['event_id']
    
    def create(self, validated_data):
        return Event.objects.create(**validated_data)
  

# TODO if keeping, maybe move this to new custom fields file
class ChildCommentHyperlinkField(serializers.HyperlinkedIdentityField):
    def get_url(self, obj, request, format):
        url_kwargs = {
            'event_id': obj.parent_event.event_id,
            'parent_comment': obj.comment_id
        }
        print('url_kwargs: ' + str(url_kwargs))
        return request.build_absolute_uri(reverse(self.view_name, kwargs=url_kwargs))
    
    
class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    summary_fields = serializers.SerializerMethodField()
    
    def get_children(self, obj):
        request = self.context.get('request')
        fmt = self.context.get('format')
        return ChildCommentHyperlinkField(
                    read_only=True, 
                    view_name='event-comment-children-list').get_url(obj, request, fmt)
    
    def get_summary_fields(self, obj):
        return {
            'number_of_children': Comment.objects.filter(parent_comment=obj.comment_id).count()
        
        }
    
    class Meta:
        model = Comment
        fields = [
            'comment_id',
            'parent_event',
            'author',
            'date_added',
            'text',
            'parent_comment',
            'children',
            'summary_fields'
        ]
        
        read_only_fields = [
            'comment_id',
            #'parent_event',
            #'author',
            'date_added',
            #'text', # allow editing the text in future? would also need date_edited
            #'parent_comment'
        ]
    
