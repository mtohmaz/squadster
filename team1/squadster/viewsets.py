import json
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.measure import Distance
from django.contrib.gis.measure import *

from squadster.serializers import *
from squadster.models import *
from squadster.authenticators import GoogleSessionAuthentication

class UserViewSet(viewsets.ModelViewSet,APIView):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    lookup_field = 'user_id'


    def create(self, request):
        serializer = UserSerializer(data=request.data)
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


class EventAttendeesViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    #lookup_field = 'event_id'

    def list(self, request, event_id, format=None):
        attendees = Event.objects.get(event_id=event_id).attendees
        serializer = UserSerializer(attendees, many=True, context={'request': request, 'format':format})

        return Response(serializer.data)

    def create(self, request, event_id):
        d = request.data
        #d['event_id'] = event_id
        # if a specific user was specified in the call, allow it?
        # should one user be able to add other users to an event? probably not
        if 'id' in d and d['id'] == request.user.id:
            user_id = d['id']
        else:
            user_id = request.user.id

        event = Event.objects.get(event_id=event_id)
        user = User.objects.get(id=user_id)
        event.attendees.add(user)

        return HttpResponseRedirect(
                reverse('event-attendees-list', kwargs={'event_id':event_id}))

    
    def destroy(self, request, event_id, user_id):
        d = request.data
        
        # TODO maybe host should be able to remove attendees from their event
        # for now limit so only user can remove them self
        if user_id != request.user.id:
            raise PermissionDenied('You are not permitted to remove other attendees')
        
        event = Event.objects.get(event_id=event_id)
        user = User.objects.get(id=user_id)
        
        # don't allow host to remove them self from attendee list
        if user_id == event.host_id:
            raise PermissionDenied('You cannot remove yourself from this event')
        
        event.attendees.remove(user)
        return 
    
    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Event.objects.get(event_id=event_id).attendees


class EventViewSet(viewsets.ModelViewSet, APIView):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventCreateSerializer
    lookup_field = 'event_id'

    def list(self, request, format=None):
        d = request.data
        d = request.GET
        if 'lat' in d and 'lon' in d and 'radius' in d:
            lat = int(d['lat'])
            lon = int(d['lon'])
            radius = int(d['radius'])
        else:
            pass
            
        
        
        search_location = GEOSGeometry('POINT('+str(lon)+' '+str(lat)+')', srid=4326)
        
        events = Event.objects.filter(
            coordinates__dwithin=(search_location, Distance(mi=radius))
        )
        
        #events = Event.objects.all()
        
        serializer = EventSerializer(
                events,
                many=True,
                context={'request': request, 'format':format})
        
        return Response(serializer.data)

    def create(self, request):
        d = request.data
        d['host'] = int(request.user.id)
        
        serializer = EventCreateSerializer(data=d, context={'request':request})
        
        if serializer.is_valid():
            event = serializer.save()
            event = Event.objects.get(event_id=event.event_id)
            
            viewserializer = EventSerializer(event, context={'request': request})
            #print(model_to_dict(event))
            return Response(viewserializer.data)
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
        
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        request['host'] = request.user.id
        event_viewset = EventViewSet()
        event_viewset.create(request)


    """
    def get_queryset(self):
        user = self.request.user
        queryset = Events.objects.filter(
            Q(host_id=user.id) | Q()
        )
    """


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'

    def list(self, request, event_id, parent_comment=None, format=None):
        req_event_id = event_id
        req_parent_comment = parent_comment
        comments = Comment.objects.filter(parent_event=req_event_id, parent_comment=req_parent_comment)

        serializer = CommentSerializer(
                comments,
                many=True,
                context={'request': request, 'format':format})
        return Response(serializer.data)

    def create(self, request, event_id):
        user = request.user
        d = request.data
        d['parent_event'] = int(event_id)
        d['author'] = user.id
        #print('d: ' + str(d))
        serializer = CommentSerializer(data=d, context={'request':request})
        if serializer.is_valid():
            comment = serializer.save()
            print('saved comment: ' + str(model_to_dict(comment)))
        else:
            return Response(serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        print('new comment: ' + str(comment))
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}


    def get_queryset(self):
        id = self.kwargs['event_id']

        return Comment.objects.filter(parent_event=id)
