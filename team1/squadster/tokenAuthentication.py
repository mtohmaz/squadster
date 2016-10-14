from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(get_user_model(), key):
        try:
            user = get_user_model().objects.get(api_key=key)
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not user.enabled:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        # This is required for the time comparison
        utc_now = datetime.utcnow()
        utc_now = utc_now.replace(tzinfo=pytz.utc)

        if token.created < utc_now - timedelta(hours=24):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token
