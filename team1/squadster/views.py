import os, datetime, logging, httplib2, json
from urllib.error import HTTPError
from datetime import datetime, timedelta
import jsonpickle

from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate
#from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

import oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt, tools, file
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from googleapiclient.discovery import build

from squadster.models import SquadsterUser, Credentials
from squadster.serializers import datetime_serializer
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
CLIENT_ID = '290427034826-un4ldmeetlngevc5ep3jnt0s71284pjf.apps.googleusercontent.com'

#should consider moving these secret files outside of project directory
credential_dir = os.path.join(os.path.dirname(__file__), 'credentials') # <- not used?
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

@csrf_exempt
def auth(request):
    if request.method == 'GET':
        return login(request)
    elif request.method == 'DELETE':
        return logout(request)

def logout(request):
    print("logging out")
    print("REQUEST" + str(jsonpickle.encode(request)))
    print("SESSION" + str(jsonpickle.encode(request.session)))
    print("SESSION KEY" + str(request.session.session_key))
    # wipe session from db
    request.session.flush()
    
    # revoke google credentials and clear from db
    credentials = Credentials.objects.get(id=request.user.id)
    credentials.credential.revoke(httplib2.Http())
    credentials.delete()
    
    return JsonResponse({'success': True})

def login(request):
    if 'google_session_token' in request.session:
        print('google_session_token in session')
        google_token = request.session['google_session_token']
        
        print ('sessionid:' + str(request.session.session_key))
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
            return HttpResponse('ID Token is invalid: ' +  str(e),status= status.HTTP_401_UNAUTHORIZED)

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
        # NOW REDIRECT TO logged-in landing page
        else:
            response = HttpResponseRedirect("/")
            #print(credentials)
            #request.session['google_session_token'] = google_token
            #response.set_cookie('google_token', google_token)
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
        return HttpResponse('ID Token is invalid: ' +  str(e),status= status.HTTP_401_UNAUTHORIZED)
    
    access_token_info = credentials.get_access_token()
    access_token = access_token_info.access_token
    expires_seconds = access_token_info.expires_in
    username = email_address.split('@')[0]
    
    try:
        print('checking if email exists')
        user = User.objects.get(email=email_address)
        print('email exists... Proceed to logged in view')
        
        #user = authenticate(email=email_address)
        #auth_login(request, user)
        
        # if already has a session,
        # set the session token to that instead of the new one
        if 'google_session_token' in request.session:
            id_token = request.session['google_session_token']

        response = HttpResponseRedirect("/")
        
        request.session['google_session_timeout'] = expires_seconds
        request.session['google_session_last_auth'] = timezone.now().strftime(settings.dateformat)
        request.session['google_session_token'] = id_token
        request.session['user_id'] = user.id
        return response
    except User.DoesNotExist as e:
        # CREATE A NEW USER RECORD
        print('email not exist')
        
        print('about to create new user')
        newUser = User.objects.create(
            username=username,
            email=email_address
        )
        Credentials.objects.create(
            id=newUser,
            credential=credentials
        )
        
        #newUser.backend='social.backends.google.GoogleOAuth2'
        newUser.backend='squadster.authenticators.GoogleSessionAuthentication'
        
        print('newUser created')
        #create api key for user and save to database
        print('about to create token')
        token = Token.objects.create(user=newUser)
        
        print('api key obtained')
        newUser.save()
        newUser.profile.save()
        
        # save session information
        request.session['google_session_timeout'] = expires_seconds
        request.session['google_session_last_auth'] = timezone.now().strftime(settings.dateformat)
        request.session['google_session_token'] = id_token
        request.session['user_id'] = newUser.id
        
        response = HttpResponseRedirect("/api/events/")
        
        #auth_login(request, user)
        
        return response



def root_view(request):
    from django.core.exceptions import PermissionDenied
    import squadster.urls
    from squadster.authenticators import GoogleSessionAuthentication
    authenticator = GoogleSessionAuthentication()
    user = authenticator.authenticate(request)
    
    if user is None:
        raise PermissionDenied()
    
    patterns = squadster.urls.urlpatterns
    
    s = jsonpickle.encode(patterns)
    print(s)
    return Response("nothing")

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

