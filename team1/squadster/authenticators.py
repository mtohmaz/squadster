from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from django.utils import timezone

from squadster.models import SquadsterUser, Admin

from datetime import datetime, timedelta

class GoogleSessionAuthentication(authentication.BaseAuthentication):
    # TODO add checking for timeout, and removing from db if timed out
    def authenticate(self, request):
        
        if 'google_token' not in request.session:
            return None
        
        
        id_token = request.session['google_token']
        
        try:
            print('GoogleSessionAuthentication: id_token=' + id_token)
            user = SquadsterUser.objects.get(google_session_token=id_token)
            
            # TODO check expiration + delete if not valid anymore, then return 
            # is_authenticated = False 
            # delete the cookie google_token
            # then Redirect to /api again
            last_auth = user.google_session_last_auth
            timeout = user.google_session_timeout
            current_time = timezone.now()
            
            if (current_time - last_auth) > timeout:
                user.google_session_token = ""
                user.google_session_last_auth = None
                user.google_session_timeout = None
                user.save()
                
                user.is_authenticated = False
                request.session.pop('google_token', None)
                print("Timeout for user: " + str(user.user.username))
                return None
                
            
            
        except SquadsterUser.DoesNotExist:
            # delete cookies somehow
            request.session.pop('google_token', None)
            raise exceptions.AuthenticationFailed('user not found')
        
        user.is_authenticated = True
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
