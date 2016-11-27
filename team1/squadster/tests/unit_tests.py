from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from squadster.viewsets import *

local = 'localhost/api'

#global test setup
class SetUp(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='user', email='user@squadster.io', password='user')

class TestEvents(SetUp):
    
    def test_get_events(self):
        request = self.factory.get(local + '/events')
        request.user = self.user

        # Test list() as if it were deployed at /events
        response = EventViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
    
    def test_create_event(self):
        request = self.factory.post(local + '/events', {'host': self.user.profile.user_id, 'title': 'test event', 'date':'12/12/12 12:12 PM', 
                                                        'max_attendees':2})
        response = EventViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.data, {'id':'1', 'title':'test event'})
        
    def test_get_event_detail(self):
        request = self.factory.get(local + '/event/1/')
        response = EventViewSet.as_view({'get':'retrieve'})(request)
        self.assertEqual(response.status_code, 200)
    
    def test_get_user_events(self):
        request = self.factory.get(local + '/users/1/events')
        response = UserEventViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
        
class TestEventComment(SetUp):
    
    def test_create_comment(self):
        request = self.factory.post(local + '/events/1/comments', {'parent_event': 1, 'author':'user'})
        response = CommentViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.data, {'comment_id':1, 'author':'user'})
    
    def test_get_event_comment(self):
        request = self.factory.get(local + '/events/1/comments')
        response = CommentViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
        
    def test_get_comment_children(self):
        request = self.factory.get(local + '/events/1/comments/1/children')
        response = CommentViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
        
    def test_get_comment_detail(self):
        request = self.factory.get(local + '/events/1/comments/1')
        response = CommentViewSet.as_view({'get':'retrieve'})(request)
        self.assertEqual(response.status_code, 200)
        
class TestEventAttendees(SetUp):
    
    def test_get_event_attendees(self):
        request = self.factory.get(local + '/events/1/attendees')
        response = EventAttendeesViewSet.as_view({'get':'list'})(request)
        self.assertEqual(response.status_code, 200)
    
    def test_join_event(self):
        request = self.factory.post(local + '/events/1/attendees', {'id': 1,})
        self.assertEqual(response.status_code, 200)
    

