
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied

from .serializers import *
from .models import *
from .authenticators import GoogleSessionAuthentication

class UserViewSet(viewsets.ModelViewSet,APIView):
    authentication_classes = (GoogleSessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = SquadsterUserSerializer
    lookup_field = 'user_id'
    
    
    def create(self, request):
        serializer = SquadsterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        # no filter right now
        # need to filter on the request parameters
        queryset = SquadsterUser.objects.all()
        return queryset


class EventViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = (GoogleSessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    lookup_field = 'event_id'
    
    
    def create(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()
            print(event)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        # no filter right now
        # need to filter on the request parameters
        queryset = Event.objects.all()
        return queryset


class UserEventViewSet(viewsets.ViewSet, APIView):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def list(self, request, user_id):
        # check current user is authorized to see these
        user = request.user
        print('request user.id: ' + str(user.id) + ' url user_id: ' + str(user_id))
        if user.id != int(user_id):
            raise PermissionDenied('You can\'t view other user\'s events')
        
        queryset = (user.hostedevents.all() | user.joinedevents.all()).order_by('date')
        #queryset = (user.hostedevents | user.joinedevents)
        
        #events_as_host = Event.objects.all() \
        #    .filter(host_id=user_id) \
        #    .order_by('date')
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    
    """
    def get_queryset(self):
        user = self.request.user
        queryset = Events.objects.filter(
            Q(host_id=user.id) | Q()
        )
    """

"""
class JoinedEventsViewSet(viewsets.ModelViewSet,APIView):
    authentication_classes = (GoogleSessionAuthentication, BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = JoinedEventsSerializer
    

    def create(self, request):
        serializer = JoinedEventsSerializer(data=request.data)
        
        if serializer.is_valid():
            joined = serializer.save()
            return Response({joined})
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        # filter to this self.request.user.get('user_id') or something similar
        queryset = JoinedEvents.objects.all()
        return queryset
"""

class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'
    
    def list(self, request, event_id):
        req_event_id = event_id
        #req_event_id = request.GET.get('event_id', '')
        #try:
        comment = get_object_or_404(Comment, parent_event=req_event_id)

        #except Comment.DoesNotExist:
        #    return Response([])
            
        #children = Comment.objects \
        #    .filter(parent_comment=req_event_id) \
        #    .order_by('date_added')
        
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
        #.select_related('parent_comment')
        
    
    def get_queryset(self):
        id = self.kwargs['event_id']
        
        return Comment.objects.filter(event_id=id)
        
        
