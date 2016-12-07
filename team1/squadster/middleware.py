"""
class SquadsterAuthMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/app/login')
        return None
"""

from django.http import HttpResponseRedirect
from squadster.authenticators import GoogleSessionAuthentication

class SquadsterAuthMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        print(request.path)
        p = request.path
        if not (p.startswith('/api/auth') or p.startswith('/api/oauth2return')) :
            auth = GoogleSessionAuthentication().authenticate(request)
            if auth is None:

                response = HttpResponseRedirect('/api/auth')
                for key in request.COOKIES:
                    response.delete_cookie(key)
                return response

        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
