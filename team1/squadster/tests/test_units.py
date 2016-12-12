import random
import requests
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from datetime import datetime, timedelta

from rest_framework.test import APIRequestFactory
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from squadster.viewsets import *
from team1 import settings

dateformat = "%Y-%m-%dT%H:%M:%S%z"
local = 'https://localhost/api'


class TestEvents(TestCase):
    #set google_session_token. Google token can be obtained from google playground
    #set google_session_last_auth. The field follows a date format
    #set google_session_timeout. Its unit is in sec
    #set user_id
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@squadster.io', password='user')
        
        client = APIClient()
        session = self.client.session
        session['google_session_token'] = 'ya29.Ci-qAyTI8yg1hps4N5niz4VI5Jhbv285Ok0LAHZs8bs3WmAFCBxZjCpnhYVe_xMEiw'
        session['google_session_last_auth'] = timezone.now().strftime(settings.dateformat)
        session['google_session_timeout'] = 4800
        session['user_id'] = self.user.id
        session['sessionid'] = self.user.id
        session.save()

    def test_get_events(self):
        response = self.client.get(local + '/events/', {'lat': 90, 'lon': '180', 'radius': 1})
        print("Resonse:" + str(response.data))
        # Test list() as if it were deployed at /events
        #response = EventViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(response.data['data']))

    def test_create_event(self):
        print ('USER ID: ' + str(self.user.id))
        id = self. user.id
        cookie = self.client.session['sessionid']
        deltaminutes = random.randint(0, 20160)
        eventtime = timezone.now() + timedelta(minutes=deltaminutes)
        event = {
                    'host_id': 1,
                    'title': 'testing',
                    'description': 'testing',
                    'lat': round(random.uniform(35,36), 6),
                    'lon': round(random.uniform(-79,-78), 6),
                    'max_attendees': 5,
                    'date': eventtime.strftime(dateformat),
                    'location': 'EB2'
                }
        response = self.client.post('https://localhost/api/events/', cookies=cookie, data=event, verify=False)
        print("Resonse:" + str(response.data))
        self.assertEqual(response.data['title'], 'testing')
"""
    def test_get_event_detail(self):
        cookie = self.client.session['sessionid']
        deltaminutes = random.randint(0, 20160)
        eventtime = timezone.now() + timedelta(minutes=deltaminutes)
        event = {
                    'host_id': 1,
                    'title': 'testing',
                    'description': 'testing',
                    'lat': round(random.uniform(35,36), 6),
                    'lon': round(random.uniform(-79,-78), 6),
                    'max_attendees': 5,
                    'date': eventtime.strftime(dateformat),
                    'location': 'EB2'
                }
        response = self.client.post('https://localhost/api/events/', cookies=cookie, data=event, verify=False)
        response = self.client.get(local + '/event/1/')
        self.assertEqual(response.data['location'], 'EB2')
        self.assertEqual(response.data['title'], 'testing')

   
    def test_get_user_events(self):
        request = self.client.get(local + '/users/1/events')
        response = UserEventViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
"""
    def test_create_comment(self):
        request = self.client.post(local + '/events/1/comments', {'parent_event': 1, 'author':'user'})
        response = CommentViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.data, {'comment_id':1, 'author':'user'})
"""
    def test_get_event_comment(self):
        request = self.client.get(local + '/events/1/comments')
        response = CommentViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
        
    def test_get_comment_children(self):
        request = self.client.get(local + '/events/1/comments/1/children')
        response = CommentViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
        
    def test_get_comment_detail(self):
        request = self.client.get(local + '/events/1/comments/1')
        response = CommentViewSet.as_view({'get':'retrieve'})(request)
        self.assertEqual(response.status_code, 200)
            
    def test_get_event_attendees(self):
        request = self.client.get(local + '/events/1/attendees')
        response = EventAttendeesViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
    
    def test_join_event(self):
        request = self.client.post(local + '/events/1/attendees', {'id': 1,})
        self.assertEqual(response.status_code, 200)
    
"""
