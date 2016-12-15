import os, datetime, logging, httplib2, json, requests
import traceback
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
from django.contrib.sessions.models import Session

import oauth2client
from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt, tools, file
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from googleapiclient.discovery import build
#from oauth2client.contrib.django_orm import Storage
from oauth2client.contrib.django_util.models import CredentialsField
#from oauth2client.contrib.django_util.models import Storage

from squadster.models import SquadsterUser, Credentials, SquadsterSession
from squadster.authenticators import GoogleSessionAuthentication
from squadster.serializers import datetime_serializer
from squadster.serializers import UserSerializer
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
#credential_dir = os.path.join(os.path.dirname(__file__), 'credentials') # <- not used?
#credential_path = os.path.join(credential_dir,'userCredentials.json')

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
def getuser(request):
    if request.method == 'GET':
        authret = GoogleSessionAuthentication().authenticate(request)
        if authret is not None:
            user = authret[0]
            return JsonResponse(UserSerializer(user).data)

@csrf_exempt
def auth(request):
    if request.method == 'GET':
        return login(request)
    elif request.method == 'DELETE':
        return logout(request)

def logout(request):
    authenticator = GoogleSessionAuthentication()
    authret = authenticator.authenticate(request)
    if authret is None:
        return HttpResponseRedirect('/app/login')
    user = authret[0]
    #print(str(user))
    print("logging out")
    print("REQUEST" + str(jsonpickle.encode(request)))
    print("SESSION" + str(jsonpickle.encode(request.session)))
    print("SESSION KEY" + str(request.session.session_key))
    # wipe session from db

    # revoke google credentials and clear from db
    #credentials = Credentials.objects.get(id=request.user.id)
    #credentials.credential.revoke(httplib2.Http())
    #credentials.delete()
    revoke_credential(user.id, request.session.get('google_access_token'))
    print('starting to clear sessions for userid: ' + str(user.id))
    squadster_sessions = SquadsterSession.objects.filter(user=user.id)
    for sqs in squadster_sessions:
        djs = sqs.session
        print('deleting session with key: ' + djs.session_key)
        sqs.delete()
        djs.delete()
    #request.session.clear()
    response = HttpResponseRedirect('/app/login')
    response.delete_cookie('sessionid')
    return response

def revoke_credential(user_id, access_token):
    try:
        #credentials = User.objects.get(id=user_id).credential
        Credentials.objects.filter(id=user_id).delete()

        #cred.credential.revoke(httplib2.Http())
        if access_token is not None:
            print('revoking token: ' + access_token)
            #token = credentials.token_response['id_token']
            r = requests.get("https://accounts.google.com/o/oauth2/revoke?token="+access_token)
    except Exception as e:
        traceback.print_exc()
        print("Exception " + str(e))
        print("credentials for user {} not found".format(user_id))

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

            request.session.clear()
            response = HttpResponseRedirect(authorize_url)
            return response
        # NOW REDIRECT TO logged-in landing page
        else:
            response = HttpResponseRedirect("/")
            # get updated credential information
            #print(credentials)
            #request.session['google_session_token'] = google_token
            #response.set_cookie('google_token', google_token)
            return response

    else:
        print('no google token in request')
        logout(request)
        # NO TOKEN GIVEN IN REQUEST, REDIRECT TO AUTHORIZE_URL
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        print('about to be redirected to google oauth2')
        return HttpResponseRedirect(authorize_url)

def update_session_from_credentials(session, credentials):
    #session = {}
    id_token = credentials.token_response['id_token']
    access_token_info = credentials.get_access_token()
    access_token = access_token_info.access_token
    print('access_token: ' + access_token)
    expires_seconds = access_token_info.expires_in

    session['google_session_timeout'] = expires_seconds
    session['google_session_last_auth'] = timezone.now().strftime(settings.dateformat)
    session['google_session_token'] = id_token
    session['google_access_token'] = access_token
    #session['user_id'] = newUser.id


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
    #print('credentials: ' + str(credentials))
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
        # JK USE THE NEW ONE
        #if 'google_session_token' in request.session:
        #    id_token = request.session['google_session_token']

        # revoke previous credential if exists
        revoke_credential(user.id, access_token)
        # store new credential
        Credentials.objects.create(
            id=user,
            credential=credentials
        )
        response = HttpResponseRedirect("/")


        request.session['user_id'] = user.id

        update_session_from_credentials(request.session, credentials)

        request.session.save()
        SquadsterSession.objects.create(
            user=user,
            session=Session.objects.get(session_key=request.session.session_key)
        )

        #request.session['google_session_timeout'] = expires_seconds
        #request.session['google_session_last_auth'] = timezone.now().strftime(settings.dateformat)
        #request.session['google_session_token'] = id_token

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
        #request.session['google_session_timeout'] = expires_seconds
        #request.session['google_session_last_auth'] = timezone.now().strftime(settings.dateformat)
        #request.session['google_session_token'] = id_token
        request.session['user_id'] = newUser.id
        update_session_from_credentials(request.session, credentials)
        request.session.create()
        SquadsterSession.objects.create(
            user=newUser,
            session=Session.objects.get(session_key=request.session.session_key)
        )

        response = HttpResponseRedirect("/")

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
