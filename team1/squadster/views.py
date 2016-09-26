	from django.shortcuts import render
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

from oauth2client import client, crypt

import os
import datetime
import logging
import httplib2
from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
#from squadster.models import CredentialsModel
from team1 import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file
import urllib.parse
from oauth2client.client import FlowExchangeError


try:
    import argparse
    flags = tools.argparser.parse_args([])
except ImportError:
    flags = None


# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

#should consider moving these secret files outside of project directory
credential_dir = os.path.join(os.path.dirname(__file__), 'credentials')
credential_path = os.path.join(credential_dir,'userCredentials.json')


FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope= ['https://www.googleapis.com/auth/calendar.readonly',
			'https://www.googleapis.com/auth/userinfo.email',
			'https://www.googleapis.com/auth/userinfo.profile',
		]
	redirect_uri='http://localhost:8000/oauth2return')

def join_event(request):
    matcher = re.search('events/([0-9]{7})/join_event', request.url)
    event_id = matcher.group(1)

    
def map(request):
    context = {'user': request.user}
    return render(request, 'map.html', context)

def login(request):
	"""Gets valid user credentials from storage.If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
	Returns:
	Credentials, the obtained credential."""
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	store = oauth2client.file.Storage(credential_path)
	credentials = store.get() 
	
	if credentials is None or credentials.invalid == True:
		FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
                                                
		authorize_url = FLOW.step1_get_authorize_url()
		return HttpResponseRedirect(authorize_url)
	else:
		get_user_info(credentials)
	"""
	Below is the code to render user's event list based on their Google Calendar:
		service = build("calendar", "v3", http=http)
		now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
		print('Getting the upcoming 10 events')
		eventsResult = service.events().list(
			calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
			orderBy='startTime').execute()
		#events = eventsResult.get('items', [])
	
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
	)
	
	return render(request, 'templates/myEvents.html', {'events':eventsResult,})
	"""
	return HttpResponseRedirect("/map")

def get_user_info(credentials):
  """Send a request to the UserInfo API to retrieve the user's information.

  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
  user_info_service = build(
      serviceName='oauth2', version='v2',
      http=credentials.authorize(httplib2.Http()))
  user_info = None
  try:
    user_info = user_info_service.userinfo().get().execute()
  except errors.HttpError, e:
    logging.error('An error occurred: %s', e)
  if user_info and user_info.get('id'):
    print (user_info)
  else:
    raise NoUserIdException()


def auth_return(request):
	#need to check for valid token before exchange, not working yet
	#if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'],request.user):
		#return  HttpResponseBadRequest()
	try:
		credentials = FLOW.step2_exchange(request.GET['code'])
		user_info = get_user_info(credentials)
		email_address = user_info.get('email')
		user_id = user_info.get('id')
		if credentials.refresh_token is not None:
			#store_credentials(user_id, credentials)
			store = oauth2client.file.Storage(credential_path)
			store.put(credentials)
			return HttpResponseRedirect("/map")
		else:
			credentials = get_stored_credentials(user_id)
			if credentials and credentials.refresh_token is not None:
				return HttpResponseRedirect("/map")
	
def store_credentials(user_id, credentials):
	
def get_stored_credentials(user_id):
