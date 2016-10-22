"""team1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from squadster import views

from squadster import viewsets

urlpatterns = [
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api$', views.login),
    url(r'^api/auth/', views.login),
    
    #url(r'^auth/', views.auth_login, name='auth_login'),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('rest_framework_social_oauth2.urls')),
    url(r'^api/admin/', admin.site.urls),
    #url(r'^map/', views.map, name='map'),
    url(r'^api/oauth2return', views.auth_return, name='oauth2return'),

    # events
    # for this and others, will probably need to look into this
    # https://docs.djangoproject.com/en/1.10/topics/http/urls/#named-groups
    url(r'^api/events/$', viewsets.EventViewSet.as_view({
            'get':'list',
            'post':'create'}),
        name='event-list'),
    url(r'^api/events/(?P<event_id>[0-9]+)$', viewsets.EventViewSet.as_view({
            'get':'retrieve'}),
        name='event-detail'),
    
    url(r'^api/events/(?P<event_id>[0-9]+)/comments/$', viewsets.CommentViewSet.as_view({
            'get':'list',
            'post':'create'}),
        name='event-comment-list'),
    
    # NEW NOT SURE IF THESE WORK
    url(r'^api/events/(?P<event_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)$', viewsets.CommentViewSet.as_view({
            'get':'retrieve'}),
        name='event-comment-detail'),
    url(r'^api/events/(?P<event_id>[0-9]+)/comments/(?P<comment_id>[0-9]+)/children/$', viewsets.CommentViewSet.as_view({
            'get':'list'}),
        name='event-comment-children-list'),
    # END NEW
    
    url(r'^api/joinedevents/$', viewsets.JoinedEventsViewSet.as_view({
            'get':'list',
            'post':'create'})),
    
    
    #url(r'^events/[0-9]{7}/join', views.join_event),
    
    
    url(r'^api/users/$', viewsets.UserViewSet.as_view({
            'get':'list',
            'post':'create'
            })),
        
    
    # TEMPORARY, REMOVE
    #url(r'^api/users/[0-9]+/apikeys/$', views.create_api_key),
    
]
