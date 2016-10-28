from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout

from squadster.models import SquadsterUser, Admin
from team1.settings import dateformat
from datetime import datetime, timedelta
import pytz

class GoogleSessionAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        #print('keys: ' + str(request.session.keys()))
        #print('items: ' + str(request.session.items()))
        
        if 'google_session_token' not in request.session \
                or 'google_session_last_auth' not in request.session \
                or 'google_session_timeout' not in request.session \
                or 'user_id' not in request.session:
            print('invalid session, login again')
            return None
        
        user_id = request.session['user_id']
        id_token = request.session['google_session_token']
        
        try:
            user = User.objects.get(id=user_id)
            
            # check expiration + delete if not valid anymore, then return 
            # is_authenticated = False 
            # delete the session
            # then Redirect to /api again
            last_auth_str = request.session['google_session_last_auth']
            last_auth = datetime.strptime(last_auth_str, dateformat)
            utctz = pytz.timezone('UTC')
            last_auth = utctz.localize(last_auth)
            timeout_seconds = request.session['google_session_timeout']
            timeout = timedelta(seconds=timeout_seconds)
            current_time = datetime.now(utctz) #timezone.now()
            
            if (current_time - last_auth) > timeout:
                request.session.clear()
                request.session.delete()
                
                print("Timeout for user: " + str(user.user.username))
                return None
                
        except SquadsterUser.DoesNotExist:
            # delete session + cookie
            request.session.flush()
            raise exceptions.AuthenticationFailed('user not found')
        
        print("GoogleSessionAuthentication succeeded")
        return (user, None)


class SquadsterAuthentication(authentication.BaseAuthentication):
    
    def authenticate(self, request):
        uid = request.user.user_id
        
        
        
        is_admin = false;
        try:
            admin = Admin.objects.get(user_id=uid)
            is_admin = true;
        except Admin.DoesNotExist:
            is_admin = false;
        
        
        
        return (user, None)

