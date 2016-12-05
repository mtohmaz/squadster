import json
import jsonpickle
import copy
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect, HttpResponseBadRequest

from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.measure import Distance
from django.contrib.gis.measure import *

from squadster import functions
from squadster.serializers import *
from squadster.models import *
from squadster.authenticators import GoogleSessionAuthentication
from squadster.permissions import *
from squadster.paginators import SquadsterPagination

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

    def list(self, request, event_id, format=None):
        attendees = Event.objects.get(event_id=event_id).attendees.all()
        page = self.paginate_queryset(attendees)
        serializer = UserSerializer(page, many=True, context={'request': request, 'format':format})
        return self.get_paginated_response(serializer.data)

    def create(self, request, event_id):
        d = copy.copy(request.data)
        #d['event_id'] = event_id
        # if a specific user was specified in the call, allow it?
        # should one user be able to add other users to an event? probably not
        if 'user_id' in d and d['user_id'] == request.user.id:
            user_id = d['user_id']
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


class EventViewSet(viewsets.ModelViewSet, viewsets.GenericViewSet):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventCreateSerializer
    pagination_class = SquadsterPagination
    lookup_field = 'event_id'

    def list(self, request, format=None):
        #d = request.data
        d = request.GET

        # location and radius is required
        if d.get('lat') and d.get('lon') and d.get('radius'):
            lat = float(d['lat'])
            lon = float(d['lon'])
            radius = int(d['radius'])
            print('Filtering events at ({},{}), radius: {}'.format(lat, lon, radius))
            # error check bounds
            if lat > 90 or lat < -90:
                return Response('lat must be in range [-90, 90]')
            elif lon > 180 or lon < -180:
                return Response('lon must be in range [-180, 180]')
            elif radius < 1 or radius > 25:
                return Response('radius must be in range [1, 25]')
            else:
                search_location = GEOSGeometry('POINT('+str(lon)+' '+str(lat)+')', srid=4326)
        else:
            return Response('Please provide lat, lon, radius.', status=400)

        # check for keywords
        if 's' in d:
            # '+' characters are converted automatically to spaces
            words = d['s'].split(' ')
        else:
            words = None

        # check for dates
        if 'startdate' in d:
            startdate = functions.str_to_time(d['startdate'])
        else:
            startdate = None

        if 'enddate' in d:
            enddate = functions.str_to_time(d['enddate'])
        else:
            enddate = None

        events = Event.objects.filter(
            coordinates__dwithin=(search_location, Distance(mi=radius))
        )
        if words is not None:
            print('filter words: ' + str(words))
            for word in words:
                events = events.filter(Q(title__contains=word) | Q(description__contains=word))

        if startdate is not None:
            events = events.filter(Q(date__gte=startdate))
        if enddate is not None:
            events = events.filter(Q(date__lte=enddate))

        page = self.paginate_queryset(events)
        serializer = EventSerializer(
                page,
                many=True,
                context={'request': request, 'format':format})
        return self.get_paginated_response(serializer.data)


    def retrieve(self, request, event_id):

        event = Event.objects.get(event_id=event_id)
        serializer = EventSerializer(event, context={'request':request})
        return Response(serializer.data)

    def create(self, request):
        d = copy.copy(request.data)
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

    #@permission_classes((IsHost,))
    def partial_update(self, request, event_id):
        d = copy.copy(request.data)
        user = request.user
        host_id = d['host']
        # can only edit events you are hosting
        if (user.id != host_id):
            raise PermissionDenied('You can\'t edit another user\'s events')
        event = self.get_queryset.get(event_id=event_id)

        serializer = EventCreateSerializer(event, data=d,
                partial=True, context={'request':request})
        if serializer.is_valid():
            newevent = serializer.save()
            return self.retrieve(request, event_id)
        else:
            return Response(serializer.errors,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        # no filter right now
        # need to filter on the request parameters
        queryset = Event.objects.all()
        return queryset


class UserHostedEventViewSet(viewsets.ViewSet, APIView):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, user_id):
        # check current user is authorized to see these
        user = request.user
        print('request user.id: ' + str(user.id) + ' url user_id: ' + str(user_id))
        if user.id != int(user_id):
            raise PermissionDenied('You can\'t view another user\'s events')

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = EventSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    """
    def create(self, request):
        request['host'] = request.user.id
        event_viewset = EventViewSet()
        event_viewset.create(request)
    """
    def get_queryset(self):
        user = self.request.user
        queryset = user.hostedevents.all().order_by('date')

class UserAttendedEventViewSet(viewsets.ViewSet, APIView):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, user_id):
        # check current user is authorized to see these
        user = request.user
        print('request user.id: ' + str(user.id) + ' url user_id: ' + str(user_id))
        if user.id != int(user_id):
            raise PermissionDenied('You can\'t view other user\'s events')

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = EventSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request):
        request['host'] = request.user.id
        event_viewset = EventViewSet()
        event_viewset.create(request)

    def get_queryset(self):
        user = self.request.user
        queryset = user.joinedevents.all().order_by('date')


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = (GoogleSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'

    def list(self, request, event_id, parent_comment=None, format=None):
        req_event_id = event_id
        req_parent_comment = parent_comment
        comments = Comment.objects.filter(parent_event=req_event_id, parent_comment=req_parent_comment)
        page = self.paginate_queryset(comments)
        serializer = CommentSerializer(
                page,
                many=True,
                context={'request': request, 'format':format})
        return self.get_paginated_response(serializer.data)

    def create(self, request, event_id):
        user = request.user
        d = copy.copy(request.data)
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
