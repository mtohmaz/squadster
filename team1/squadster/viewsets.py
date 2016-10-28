
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

from squadster.serializers import *
from squadster.models import *
from squadster.authenticators import GoogleSessionAuthentication

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
    
    def list(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True, context={'request': request, 'format':format})
        
        return Response(serializer.data)
    
    def create(self, request):
        d = request.data.dict()
        d['host_id'] = int(request.user.id)
        
        serializer = EventSerializer(data=d)
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
        
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        request['host_id'] = request.user.id
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
        
        serializer = CommentSerializer(comments, many=True, context={'request': request, 'format':format})
        return Response(serializer.data)
    
    def create(self, request, event_id):
        user = request.user
        d = request.data.dict()
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
        
        
