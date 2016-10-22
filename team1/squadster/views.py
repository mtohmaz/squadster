import os, datetime, logging
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


from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.six import BytesIO
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt, tools, file
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from googleapiclient.discovery import build

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
CLIENT_ID = '765648849014-kjgtsiqvfmkinasvc5tak562hr7k92sj.apps.googleusercontent.com'

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
    from oauth2client import client, crypt

    print('request:' + str(request))
    """
    if request.user.is_authenticated:
        response = HttpResponseRedirect("/api/events/")
        return response
    else:
        FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, request.user)
            
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    """
    
    #if 'google_token' in request.META:
    if 'google_token' in request.COOKIES:
        print('google token in request')
        google_token = request.COOKIES.get('google_token')
        #google_token = request.session['google_token']
        # TODO ASK GOOGLE IF ITS VALID
        # (Receive token by HTTPS POST)
        print ('google token:' + str(google_token))
        try:
            idinfo = client.verify_id_token(google_token, CLIENT_ID)
            # If multiple clients access the backend server:
            if idinfo['aud'] not in [CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            if idinfo['hd'] != 'ncsu.edu':
                raise crypt.AppIdentityError("Wrong hosted domain.")
        except crypt.AppIdentityError as e:
            # Invalid token
            return HttpResponse('Token ID is invalid: ' +  str(e),status= status.HTTP_401_UNAUTHORIZED)
        
        userid = idinfo['sub']
        # IF IT IS:
        # CHECK IF USER EMAIL EXISTS IN DATABASE
        user = get_user_model().objects.filter(email=idinfo['email'])
        # IF NOT, REDIRECT TO AUTHORIZE_URL
        if user is None :
            FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, request.user)
            
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        # NOW REDIRECT TO list-view
        else:
            response = HttpResponseRedirect("/api/events/")
            #print(credentials)
            #request.session['google_token'] = credentials.get_access_token().access_token
            response.set_cookie('google_token', google_token)
            return response
            
    else:
        print('no google token in request')
        # NO TOKEN GIVEN IN REQUEST, REDIRECT TO AUTHORIZE_URL
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        print('about to be redirected to google oauth2')
        return HttpResponseRedirect(authorize_url)


def get_user_info(credentials):
    user_info_service = build(serviceName='oauth2', version='v2', http=credentials.authorize(httplib2.Http()))
    user_info = None
    try:
        user_info = user_info_service.userinfo().get().execute()
        print ('line1')
    except HTTPError as e:
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        return user_info
    else:
        raise NoUserIdException()
  



def auth_return(request):
    credentials = FLOW.step2_exchange(request.GET['code'])
    user_info = get_user_info(credentials)
    email_address = user_info.get('email')
    user_id = user_info.get('id')
    
    # CHECK IF IN DATABASE YET, IF NOT, CREATE ENTRY
    print('credentials: ' + str(credentials))
    print('user_info: ' + str(user_info))
    print('id_token: ' + str(credentials.id_token))
    id_token = credentials.token_response['id_token']
    
    
    try:
        idinfo = client.verify_id_token(id_token, CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        if idinfo['hd'] != 'ncsu.edu':
            raise crypt.AppIdentityError("Wrong hosted domain.")
    except crypt.AppIdentityError as e:
        # Invalid token
        return HttpResponse('Token ID is invalid: ' +  str(e),status= status.HTTP_401_UNAUTHORIZED)
    
    
    
    try:
        print('checking if email exists')
        user = User.objects.get(email=email_address)
        print('email exist... Proceed to list-view')
        
        #user = authenticate(email=email_address)
        #auth_login(request, user)
        
        # TODO if user.profile.google_session_token already exists,
        # set the session token to that instead of the new one
        
        if user.profile.google_session_token:
            id_token = user.profile.google_session_token
        
        response = HttpResponseRedirect("/api/events/")
        response.set_cookie('google_token', id_token)
        return response
    except User.DoesNotExist as e:
        # CREATE A NEW USER RECORD
        print('email not exist')
        access_token_info = credentials.get_access_token()
        print(access_token_info)
        access_token = access_token_info.access_token
        expires_seconds = access_token_info.expires_in
        
        username = email_address.split('@')[0]
        print('about to create new user')
        newUser = User.objects.create(
            username=username,
            email=email_address
        )
        newUser.backend='social.backends.google.GoogleOAuth2'
        
        print('newUser created')
        #create api key for user and save to database
        from rest_framework.authtoken.models import Token
        print('about to create token')
        token = Token.objects.create(user=newUser)
        
        print('api key obtained')
        newUser.save()

        newUser.profile.google_session_token = id_token
        newUser.profile.google_session_timeout = timedelta(seconds=expires_seconds)
        newUser.profile.google_session_last_auth = timezone.now()
        newUser.profile.save()
        
        response = HttpResponseRedirect("/api/events/")
        
        #user = authenticate(username=newUser.username)
        #auth_login(request, user)
        
        response.set_cookie('google_token', id_token)
        return response


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
"""



"""
    squadsteruser: a SquadsterUser object
"""

