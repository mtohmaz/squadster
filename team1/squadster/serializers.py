from rest_framework import serializers

from .models import Event, SquadsterUser


class SquadsterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SquadsterUser
        fields = [
            'user_id',
            'email',
            'enabled']
        read_only_fields = ['user_id', 'enabled']
    
    def create(self, validated_data):
        return SquadsterUser.objects.create(**validated_data)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'event_id',
            'host_id',
            'title',
            'date',
            'max_attendees']
        read_only_fields = ['event_id']
    
    def create(self, validated_data):
        return Event.objects.create(**validated_data)


class EventSearchSerializer(serializers.Serializer):
    start_date = serializers.DateTimeField()
    host_id = serializers.IntegerField()
    end_date = serializers.DateTimeField()
    description = serializers.CharField(max_length=250)
    max_attendees = serializers.IntegerField()
    
