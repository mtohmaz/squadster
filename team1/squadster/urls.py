
from django.conf.urls import url, include
#from django.contrib import admin

from squadster import views
#import squadster
from squadster import viewsets

urlpatterns = [
    url(r'^session/', views.getuser), # basically a ping target to check if logged in
    url(r'^auth/', views.auth),
    url(r'^oauth2return', views.auth_return, name='oauth2return'),

    # EVENTS
    url(r'^events/$', viewsets.EventViewSet.as_view({
            'get':'list',
            'post':'create'}),
        name='event-list'),
    url(r'^events/(?P<event_id>[0-9]+)$', viewsets.EventViewSet.as_view({
            'get':'retrieve',
            'patch':'partial_update'}),
        name='event-detail'),


    # EVENT COMMENTS
    url(r'^events/(?P<event_id>[0-9]+)/comments/$', viewsets.CommentViewSet.as_view({
            'get':'list',
            'post':'create'}),
        name='event-comment-list'),
    url(r'^events/(?P<event_id>[0-9]+)/comments/(?P<parent_comment>[0-9]+)/children/$', viewsets.CommentViewSet.as_view({
            'get':'list'}),
        name='event-comment-children-list'),
    url(r'^events/(?P<event_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)$', viewsets.CommentViewSet.as_view({
            'get':'retrieve'}),
        name='event-comment-detail'),

    # EVENT ATTENDANCE
    url(r'^events/(?P<event_id>[0-9]+)/attendees/$', viewsets.EventAttendeesViewSet.as_view({
            'get':'list',
            'post':'create',
        }),
        name='event-attendees-list'),
    url(r'^events/(?P<event_id>[0-9]+)/attendees/(?P<user_id>[0-9]+)$', viewsets.EventAttendeesViewSet.as_view({
            'delete':'destroy'
    }), name='event-attendees-detail'),


    # USERS
    url(r'^users/$', viewsets.UserViewSet.as_view({
            'get':'list',
    })),
    url(r'^users/(?P<user_id>[0-9]+)/hostedevents/', viewsets.UserHostedEventViewSet.as_view({
        'get':'list'
    })),
    url(r'^users/(?P<user_id>[0-9]+)/attendedevents/', viewsets.UserAttendedEventViewSet.as_view({
        'get':'list'
    })),

    # TEMPORARY, REMOVE
    #url(r'^api/users/[0-9]+/apikeys/$', views.create_api_key),
]
