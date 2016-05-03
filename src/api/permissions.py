from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from oauth2_provider.ext.rest_framework import OAuth2Authentication, \
                                               TokenHasScope, \
                                               TokenHasReadWriteScope


class WeakTokenHasScope(TokenHasScope):
    """
    DRF permission class for mixed OAuth and session support.

    Checks whether request has an access token with the scopes listed in
    required_scopes, defined as a class variable of the view. Skips the check
    if the request isn't authenticated via OAuth.
    """

    def has_permission(self, request, view):
        # Only check scopes for OAuth 2.0 requests.
        # Allow users with a valid session to browse the API.
        if not isinstance(request.successful_authenticator,
                          OAuth2Authentication):
            return True

        return super(WeakTokenHasScope, self).has_permission(request, view)
        #return True


class WeakTokenHasReadWriteScope(TokenHasReadWriteScope):
    """
    DRF permission class for mixed OAuth and session support.

    Checks whether request has an access token with the scopes listed in
    required_scopes, defined as a class variable of the view. Skips the check
    if the request isn't authenticated via OAuth.

    Additionally requires that requests using safe methods (GET, OPTIONS, HEAD)
    have the 'read' scope and unsafe methods (POST, PUT, PATCH, DELETE) have
    the 'write' scope. Those scopes can be customized with
    OAUTH2_PROVIDER.READ_SCOPE and OAUTH2_PROVIDER.WRITE_SCOPE.
    """

    def has_permission(self, request, view):
        # Only check scopes for OAuth 2.0 requests.
        # Allow users with a valid session to browse the API.
        if not isinstance(request.successful_authenticator,
                          OAuth2Authentication):
            return True

        return super(WeakTokenHasReadWriteScope, self).has_permission(
            request, view)
        #return True


#class benchmarkTestAuthentication(authentication.BaseAuthentication):
#
#    def authenticate(self, request):
#        try:
#            user = User.objects.get(username="ddd")
#        except User.DoesNotExist:
#            raise exceptions.AuthenticationFailed('No such user')
#
#        return (user, None)