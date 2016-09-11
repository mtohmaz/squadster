from django.shortcuts import render
from django.http import HttpResponse
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

## python-social-auth
from social.backends.oauth import BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa
##

"""
def login(request):
    context = {'user': request.user}
    return render(request, 'login.html', context)
"""

def join_event(request):
    matcher = re.search('events/([0-9]{7})/join_event', request.url)
    event_id = matcher.group(1)

def map(request):
    context = {'user': request.user}
    return render(request, 'map.html', context)



@psa('social:complete')
def home(request):
    if isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')
