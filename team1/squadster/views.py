from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.contrib.auth import logout as auth_logout, login

from oauth2client.client import flow_from_clientsecrets
from oauth2client import client, crypt
import os

## models
from .models import Event
from .serializers import EventSerializer

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
    redirect_uri='http://localhost:8000/oauth2return')


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


def auth_return(request):
    #need to check for valid token before exchange, not working yet
    #if not xsrfutil.validate_token(settings.SECRET_KEY, request.GET['state'],request.user):
        #return  HttpResponseBadRequest()
    #try:
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



def home(request):
    email = request.COOKIES.get("email")
    sess_id = request.COOKIES.get("id_token")
    
    if check_authentication(email, sess_id):
        pass
    else:
        return render(request, 'login.html')


def check_authentication(request):
    token = ''
    print(request)
    return False
    """try:
        idinfo = client.verify_id_token(token, CLIENT_ID)
        # If multiple clients access the backend server:
        if idinfo['aud'] not in [ANDROID_CLIENT_ID, IOS_CLIENT_ID, WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
        if idinfo['hd'] != APPS_DOMAIN_NAME:
            raise crypt.AppIdentityError("Wrong hosted domain.")
    except crypt.AppIdentityError:
        # Invalid token
        return False
    userid = idinfo['sub']
    print(userid)
    return True"""
    #return HttpResponse(json.dumps(userid), mimetype='application/json')
    
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
    except (errors.HttpError, e):
        logging.error('An error occurred: %s', e)
    if user_info and user_info.get('id'):
        print (user_info)
    else:
        raise NoUserIdException()



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
        # query database for events with parameters
    else:
        # return failure
        print("invalid http method")
    
    
    print(request)
    return JsonResponse({'hello': 'world'})
