from django.shortcuts import render
from django.http import HttpResponse


from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login

from oauth2client import client, crypt

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

def home(request):
    if check_authentication(request):
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
    return True
    #return HttpResponse(json.dumps(userid), mimetype='application/json')
    """

def auth_login(request):
    print(request)
    
