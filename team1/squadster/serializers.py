from rest_framework import serializers

from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'event_id',
            'title',
            'date',
            'max_attendees']
        read_only_fields = ['event_id']

class EventSearchSerializer(serializers.Serializer)
    start_date = serializers.DateTimeField()
    host_id = serializers.IntegerField()
    end_date = serializers.DateTimeField()
    description = serializers.CharField(max_length=250)
    max_attendees = serializers.IntegerField()
    
