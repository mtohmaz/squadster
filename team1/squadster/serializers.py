
from rest_framework import serializers
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry

from squadster.models import *

def datetime_serializer(obj):
    return obj.isoformat()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'email']
        read_only_fields = ['user_id']
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)


# FOR WRITING EVENTS
class EventCreateSerializer(serializers.ModelSerializer):
    lat = serializers.DecimalField(max_digits=14, decimal_places=10)
    lon = serializers.DecimalField(max_digits=14, decimal_places=10)
    class Meta:
        model = Event
        fields = [
            'event_id',
            'host',
            'title',
            'date',
            'max_attendees',
            'description',
            'lat',
            'lon',
            'location'
        ]
        read_only_fields = ['event_id']
    
    def create(self, validated_data):
        lat = validated_data['lat']
        lon = validated_data['lon']
        coordinates = GEOSGeometry('POINT('+str(lon)+' '+str(lat)+')', srid=4326)
        validated_data['coordinates'] = coordinates
        validated_data.pop('lat')
        validated_data.pop('lon')
        return Event.objects.create(**validated_data) 
        
# FOR READING EVENTS
class EventSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    summary_fields = serializers.SerializerMethodField()
    attendees = serializers.SerializerMethodField()
    coordinates = serializers.SerializerMethodField()
    
    def get_coordinates(self, event):
        pnt = event.coordinates
        s = '[{}, {}]'.format(pnt.x, pnt.y)
        return s
        
    def get_comments(self, event):
        request = self.context['request']
        return request.build_absolute_uri(
            reverse('event-comment-list', kwargs={'event_id':event.event_id}))
    
    def get_attendees(self, event):
        request = self.context['request']
        return request.build_absolute_uri(
            reverse('event-attendees-list', kwargs={'event_id':event.event_id}))
    
    def get_summary_fields(self, obj):
        return {
            'host_email': User.objects.get(id=obj.host.id).email,
            'number_of_comments': Comment.objects.filter(parent_event=obj.event_id).count()
        }
    
    class Meta:
        model = Event
        fields = [
            'event_id',
            'host',
            'title',
            'date',
            'max_attendees',
            'description',
            'comments',
            'attendees',
            'summary_fields',
            'coordinates',
            'location'
        ]
        read_only_fields = ['event_id']
  

# TODO if keeping, maybe move this to new custom fields file, or just integrate in CommentSerializer
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
    
