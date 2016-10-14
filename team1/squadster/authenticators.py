from rest_framework import authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from squadster.models import SquadsterUser

class GoogleSessionAuthentication(authentication.BaseAuthentication):
    # TODO add checking for timeout, and removing from db if timed out
    def authenticate(self, request):
        id_token = request.COOKIES.get('google_token')
        print('GoogleSessionAuthentication: id_token=' + id_token)
        if not id_token:
            return None
        
        try:
            user = SquadsterUser.objects.get(google_session_token=id_token)
        except SquadsterUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('user not found')
        
        return (user, None)