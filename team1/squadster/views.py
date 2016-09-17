from django.shortcuts import render
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

from oauth2client import client, crypt

import os
import logging
import httplib2from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django_sample.plus.models import CredentialsModel
from django_sample import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/calender.readonly',
	redirect_uri='http://localhost:8000/oauth2return')
"""
## python-social-auth
from social.backends.oauth import BaseOAuth2
from social.backends.google import GooglePlusAuth
from social.backends.utils import load_backends
from social.apps.django_app.utils import psa
##
"""

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


"""
@psa('social:complete')
def home(request, backend):
    if isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)
    data = {'id': user.id, 'username': user.username}
    return HttpResponse(json.dumps(data), mimetype='application/json')
"""
@login_required
def home(request):
	#get user's token from database
	storage = Storage(CredentialsModel, 'id', request.user, 'credential')
	credential = storage.get()
	#if user's token is not found, it's a new user, 
	if credential is None or credential.invalid == True:
		FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
		authorize_url = FLOW.step1_get_authorize_url()
		return HttpResponseRedirect(authorize_url)
	else:
		http = httplib2.Http()
		http = credential.authorize(http)
		service = build("calender", "v3", http=http)
		now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
		print('Getting the upcoming 10 events')
		eventsResult = service.events().list(
			calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
			orderBy='startTime').execute()
		#events = eventsResult.get('items', [])
	"""
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
	)
	"""

    return render(request, 'templates/myEvents.html', 'events':eventsResult)


@login_required
def auth_return(request):
    print(request)
    if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
                                 request.user):
		return  HttpResponseBadRequest()
		credential = FLOW.step2_exchange(request.REQUEST)
		#store user's credential to database
		storage = Storage(CredentialsModel, 'id', request.user, 'credential')
		storage.put(credential)
	return HttpResponseRedirect("/")
    
