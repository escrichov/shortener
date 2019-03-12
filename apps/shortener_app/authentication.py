from rest_framework import authentication
from rest_framework import exceptions
from .models import APIAccess


class APIAccessAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        apikey = request.META.get('HTTP_X_API_KEY')
        if not apikey:
            return None

        try:
            api_access = APIAccess.objects.get(apikey=apikey)
        except APIAccess.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (api_access.user, None)
