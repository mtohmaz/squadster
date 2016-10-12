import os
import datetime
import logging
import httplib2
import urllib.parse
from urllib.error import HTTPError
from datetime import datetime, timedelta

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.six import BytesIO
from django.contrib.auth import logout as auth_logout, login
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

import oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt
from oauth2client import client
from oauth2client import tools
from oauth2client import file
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from googleapiclient.discovery import build

#from squadster.models import CredentialsModel
from squadster.models import SquadsterUser
from team1 import settings



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
        ],
    redirect_uri='http://localhost/api/oauth2return')
    
def home(request):
    pass

def login(request):
    """Send a request to the UserInfo API to retrieve the user's information.
  Args:
    credentials: oauth2client.client.OAuth2Credentials instance to authorize the
                 request.
  Returns:
    User information as a dict.
  """
    print('request:')
    print(request)
    if 'google_token' in request.META:
        google_token = request.META['google_token']
        
        
        
        # TODO ASK GOOGLE IF ITS VALID
            # IF IT IS:
                # CHECK IF USER EMAIL EXISTS IN DATABASE
                    # IF NOT, ADD RECORD (and api key)
                # NOW REDIRECT TO list-view
            # IF NOT, REDIRECT TO AUTHORIZE_URL
            
    else:
        pass
        # NO TOKEN GIVEN IN REQUEST, REDIRECT TO AUTHORIZE_URL
    
    
    
    # TODO CHECK HERE IF USER EMAIL EXISTS & MAKE ENTRY IF NOT, 
    #    THEN REDIRECT TO list-view
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get() 
    
    
    # CHECK IF SESSION IS VALID THROUGH CALL TO GOOGLE
    #   IF YES, REDIRECT TO list-view
    #   IF NO, REDIRECT TO AUTHORIZE_URL
    print('line0')
    if credentials is None or credentials.invalid == True:
        print('line0.3')
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
                                                
        authorize_url = FLOW.step1_get_authorize_url()
        print('line0.4')
        print(authorize_url)
        return HttpResponseRedirect(authorize_url)
    else:
        print('line0.1')
        get_user_info(credentials)
        print('line0.2')
    return HttpResponseRedirect("/list-view")


def get_user_info(credentials):
    user_info_service = build(serviceName='oauth2', version='v2', http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
        print ('line1')
    except HTTPError as e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        print (user_info)
        print ('line2')
        return user_info
    else:
        raise NoUserIdException()
  



def auth_return(request):
    from .models import SquadsterUser
    #need to check for valid token before exchange, not working yet
    #if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'],request.user):
        #return  HttpResponseBadRequest()
    credentials = FLOW.step2_exchange(request.GET['code'])
    print ('line3')
    user_info = get_user_info(credentials)
    print ('line4')
    email_address = user_info.get('email')
    user_id = user_info.get('id')
    
    #store = oauth2client.file.Storage(credential_path)
    #store.put(credentials)
    
    # CHECK IF IN DATABASE YET, IF NOT, CREATE ENTRY
    print('credentials: ' + str(credentials))
    print('user_info: ' + str(user_info))
    
    
    try:
        user = SquadsterUser.objects.get(email=email_address)
    except ObjectDoesNotExist as e:
        # CREATE A NEW USER RECORD
        access_token_info = credentials.get_access_token()
        print(access_token_info)
        access_token = access_token_info.access_token
        expires_seconds = access_token_info.expires_in
        
        
        user = SquadsterUser.objects.create(
            email=email_address,
            # TODO api_key
            api_key="",
            google_session_token=access_token,
            google_session_timeout=timedelta(seconds=expires_seconds),
            google_session_last_auth=timezone.now()
        )
        #print(e)
    
    return HttpResponseRedirect("/list-view")

    
        

def store_credentials(user_id, email):
    print('something')
    
def get_stored_credentials(user_id):
    print('something')
    
def create_event(request):
    print('something')
"""
def map(request):
    print('line5')
    login(request)
    print('line6')
    context = {'user': request.user}
    return render(request, 'map.html', context)

@csrf_exempt
def my_events(request):
    if request.method == 'GET':
        events = []

        for event in Event.objects.filter(active=True).order_by('date'):
            events.append(str(event))

        return HttpResponse(json.dumps(events), content_type='text/json',
            status=200)
    else: 
        return HttpResponse(json.dumps('Forbidden'), content_type='text/json', 
    status=403)

@csrf_exempt
def events(request):
    if request.method == "POST":
        print("got a post")
        
        stream = BytesIO(request.body)
        data = JSONParser().parse(stream)
        
        validator = EventSerializer(data=data)
        if validator.is_valid():
            stored = validator.save()
            print(stored)
        else:
            print("INVALID EVENT")
            print(validator.errors)
        
        
        # enter data
        # return success/failure response
    elif request.method == "GET":
        print("got a GET")
        ret = []
        for event in Event.objects.all():
            serializers = EventSerializer(event)
            print(serializers.data)
        # query database for events with parameters
    else:
        # return failure
        print("invalid http method")
    
    
    print(request)
    return JsonResponse({'hello': 'world'})
"""


"""
    squadsteruser: a SquadsterUser object
"""

@csrf_exempt
def create_api_key(squadsteruser):
    from rest_framework.authtoken.models import Token
    
    token = Token.objects.create(user=squadsteruser)
    print(token.key)

def get_api_key(user_id):
    pass
    

