from rest_framework import permissions, \
                           authentication
from oauth2_provider.ext.rest_framework import OAuth2Authentication, \
                                               TokenHasScope, \
                                               TokenHasReadWriteScope

from inventory.models import Card

from django.contrib.auth.models import User
from django.conf import settings


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


def _card_is_public(repo_base, repo_name, card_name):
    """Returns True if card exists and is public, False otherwise."""
    try:
        card = Card.objects.get(
            repo_base=repo_base,
            repo_name=repo_name,
            card_name=card_name)
        if card.public is not False:
            return True
    except Card.DoesNotExist:
        pass

    return False


class PublicCardPermission(permissions.BasePermission):
    """
    Returns True if the card exists and is public.

    Only allows safe methods: GET, OPTIONS, and HEAD.
    """

    def has_permission(self, request, view):
        params = request.parser_context['kwargs']
        if (request.method in permissions.SAFE_METHODS and
            _card_is_public(repo_base=params['repo_base'],
                            repo_name=params['repo_name'],
                            card_name=params['card_name'])):
            return True

        return False


class PublicCardAuthentication(authentication.BaseAuthentication):
    """
    Returns anonymous user if the card exists and is public.

    Only allows safe methods: GET, OPTIONS, and HEAD.
    """

    def authenticate(self, request):
        params = request.parser_context['kwargs']
        if (request.method in permissions.SAFE_METHODS and
            _card_is_public(repo_base=params['repo_base'],
                            repo_name=params['repo_name'],
                            card_name=params['card_name'])):
            user = User.objects.get(username=settings.ANONYMOUS_ROLE)
            return (user, None)

        return None
