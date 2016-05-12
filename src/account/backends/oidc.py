from social.backends.open_id import OpenIdConnectAuth
from social.exceptions import AuthTokenError

import datetime
import six
import time
from calendar import timegm

from jwkest import JWKESTException
from jwkest.jwk import KEYS
from jwkest.jws import JWS


class _cache(object):
    """
    Caches method return values for a specific length of time.

    Maintains one cache per class, so subclasses have a different cache entry
    for the same cached method.

    Does not work for methods with arguments.
    """

    def __init__(self, ttl):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, fn):
        def wrapped(this):
            now = time.time()
            last_updated = None
            cached_value = None
            if this.__class__ in self.cache:
                last_updated, cached_value = self.cache[this.__class__]
            if not cached_value or now - last_updated > self.ttl:
                try:
                    cached_value = fn(this)
                    self.cache[this.__class__] = (now, cached_value)
                except:
                    # Use previously cached value when call fails, if available
                    if not cached_value:
                        raise
            return cached_value
        return wrapped


def _autoconf(name):
    """fget helper function to fetch values from the OIDC config."""
    def getter(self):
        return self.oidc_config().get(name)
    return getter


class DataHubFixedOpenIdConnect(OpenIdConnectAuth):
    """
    Broader OpenID Connect support than what comes with PSA out of the box.

    This is based on from https://github.com/omab/python-social-auth/pull/747,
    an unmerged pull request on Python Social Auth.

    PSA 0.2.13's OIDC support is very specific to Google's OIDC server. It
    only supports HS256 signed tokens, doesn't handle signed userinfo
    responses, and doesn't handle situations where the OIDC server's clock is
    ahead of the client's. The pull request is also very specific and has some
    security vulnerabilities that this fixes.

    To use this, override these constants in a subclass:

        OIDC_URL
        DEFAULT_SCOPE
        ID_KEY
        USERNAME_KEY
        CLOCK_LEEWAY

    And set these constants in your project's settings based on your OIDC
    client registration:

        SOCIAL_AUTH_{backend_name}_KEY = OAuth client id
        SOCIAL_AUTH_{backend_name}_SECRET = OAuth client secret
        (SOCIAL_AUTH_{backend_name}_ID_TOKEN_DECRYPTION_KEY =
            SOCIAL_AUTH_{backend_name}_SECRET)
        SOCIAL_AUTH_{backend_name}_TOKEN_SIGNING_ALGORITHM = ''
        SOCIAL_AUTH_{backend_name}_USERINFO_SIGNING_ALGORITHM = ''
    """

    OIDC_URL = None
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'sub'
    USERNAME_KEY = 'preferred_username'
    DEFAULT_SCOPE = ['openid', 'email', 'profile']
    # Amount of acceptable clock skew between IdP and this server in seconds.
    # 5 minutes
    CLOCK_LEEWAY = 300

    @_cache(ttl=86400)
    def oidc_config(self):
        """
        Discovers the IdP's OIDC configuration.

        Response is cached for 24 hours.
        """
        return self.get_json(self.OIDC_URL +
                             '/.well-known/openid-configuration')

    ID_TOKEN_ISSUER = property(_autoconf('issuer'))
    ACCESS_TOKEN_URL = property(_autoconf('token_endpoint'))
    AUTHORIZATION_URL = property(_autoconf('authorization_endpoint'))
    REVOKE_TOKEN_URL = property(_autoconf('revocation_endpoint'))
    USERINFO_URL = property(_autoconf('userinfo_endpoint'))
    JWKS_URI = property(_autoconf('jwks_uri'))

    @_cache(ttl=86400)
    def get_jwks_keys(self):
        """
        Returns the keys used by the IdP.

        Merges client secret into JWK set from server
        Response is cached for 24 hours.
        """
        keys = KEYS()
        keys.load_from_url(self.JWKS_URI)

        # Add client secret as oct key so it can be used for HMAC signatures
        _client_id, client_secret = self.get_key_and_secret()
        keys.add({'key': client_secret, 'kty': 'oct'})
        return keys

    def get_nonce(self, nonce):
        """
        Returns the PSA Association object matching a nonce or None.

        Overridden from PSA default for OpenIdConnectAuth because there's a
        bug in 0.2.13 where it checked the nonce used for the ACCESS_TOKEN_URL
        instead of the AUTHORIZATION_URL.

        Used when verifying a request isn't a replay attack. A better name
        would be get_association_for_nonce(), but this is what PSA uses.
        """
        try:
            # PSA 0.2.13 checks the nonce against the ACCESS_TOKEN_URL, but
            # that's the wrong nonce to check.
            return self.strategy.storage.association.get(
                server_url=self.AUTHORIZATION_URL,
                handle=nonce
            )[0]
        except IndexError:
            pass

    def validate_userinfo_claims(self, jwt):
        if jwt['iss'] != self.ID_TOKEN_ISSUER:
            raise AuthTokenError(self, 'Invalid issuer')

        if 'sub' not in jwt:
            raise AuthTokenError(self, 'Missing subject')

        client_id, _client_secret = self.get_key_and_secret()
        if isinstance(jwt['aud'], six.string_types):
            jwt['aud'] = [jwt['aud']]
        if client_id not in jwt['aud']:
            raise AuthTokenError(self, 'Invalid audience')

        # Verify this jwt was issued in the last x minutes.
        utc_timestamp = timegm(datetime.datetime.utcnow().utctimetuple())
        if abs(utc_timestamp - jwt['iat']) > self.CLOCK_LEEWAY:
            raise AuthTokenError(self, 'Incorrect userinfo jwt: iat')

    def _validate_id_token_audience(self, id_token):
        client_id, _client_secret = self.get_key_and_secret()
        if isinstance(id_token['aud'], six.string_types):
            id_token['aud'] = [id_token['aud']]
        if client_id not in id_token['aud']:
            raise AuthTokenError(self, 'Invalid audience')

        # Pretty sure this is wrong. Text of spec says "This Claim is only
        # needed when the ID Token has a single audience value and that
        # audience is different than the authorized party."
        if len(id_token['aud']) > 1 and 'azp' not in id_token:
            raise AuthTokenError(self, 'Incorrect id_token: azp')

        if 'azp' in id_token and id_token['azp'] != client_id:
            raise AuthTokenError(self, 'Incorrect id_token: azp')

    def _validate_id_token_times(self, id_token):
        utc_timestamp = timegm(datetime.datetime.utcnow().utctimetuple())
        # Verify the token has no expired yet, with x minutes leeway.
        if utc_timestamp > id_token['exp'] + self.CLOCK_LEEWAY:
            raise AuthTokenError(self, 'Signature has expired')

        if ('nbf' in id_token and
                utc_timestamp < id_token['nbf'] - self.CLOCK_LEEWAY):
            raise AuthTokenError(self, 'Incorrect id_token: nbf')

        # Verify the token was issued in the last x minutes.
        if abs(utc_timestamp - id_token['iat']) > self.CLOCK_LEEWAY:
            raise AuthTokenError(self, 'Incorrect id_token: iat')

    def validate_id_token_claims(self, id_token):
        if id_token['iss'] != self.ID_TOKEN_ISSUER:
            raise AuthTokenError(self, 'Invalid issuer')

        if 'sub' not in id_token:
            raise AuthTokenError(self, 'Missing subject')

        self._validate_id_token_audience(id_token)

        self._validate_id_token_times(id_token)

        # Validate the nonce to ensure the request was not modified
        nonce = id_token.get('nonce')
        if not nonce:
            raise AuthTokenError(self, 'Incorrect id_token: nonce')

        nonce_obj = self.get_nonce(nonce)
        if nonce_obj:
            self.remove_nonce(nonce_obj.id)
        else:
            raise AuthTokenError(self, 'Incorrect id_token: nonce')

    def user_data(self, access_token, *args, **kwargs):
        """
        Returns a user's details from the userinfo endpoint.

        Called by PSA when building info about a user.
        """
        # TODO: Extend https://github.com/omab/python-social-auth/pull/747
        # to include a better version of this -- one which treats the response
        # as json if the Content-Type is application/json and treats it as a
        # JWS needing to be verified as below if it's application/jwt.
        #
        # To support all servers, that should also support JWEs.
        #
        # When PSA is eventually improves its OIDC support, this file can be
        # simplified.
        response = self.request(self.USERINFO_URL,
                                headers={'Authorization':
                                         'Bearer {0}'.format(access_token)})
        jws = response.content
        try:
            # Decode the JWT and raise an error if the sig is invalid.
            # Make sure to specify the expected algorithm to prevent attacks
            # that use an RSA public key as an HMAC secret key.
            user_info = JWS().verify_compact(
                jws.encode('utf-8'),
                keys=self.get_jwks_keys(),
                sigalg=self.setting('USERINFO_SIGNING_ALGORITHM'))
        except JWKESTException as e:
            raise AuthTokenError(
                self, ('User info error: Signature verification failed. '
                       'Reason: {0}'.format(e)))
        self.validate_userinfo_claims(user_info)
        return user_info

    def get_user_details(self, response):
        username_key = self.setting('USERNAME_KEY', default=self.USERNAME_KEY)
        return {
            'username': response.get(username_key),
            'email': response.get('email'),
            'fullname': response.get('name'),
            'first_name': response.get('given_name'),
            'last_name': response.get('family_name'),
        }

    def validate_and_return_id_token(self, jws):
        """
        Validates the id_token according to the spec.

        http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation.
        """
        try:
            # Decode the JWT and raise an error if the sig is invalid.
            # Make sure to specify the expected algorithm to prevent attacks
            # that used an RSA public key as an HMAC secret key.
            id_token = JWS().verify_compact(
                jws.encode('utf-8'),
                keys=self.get_jwks_keys(),
                sigalg=self.setting('TOKEN_SIGNING_ALGORITHM'))
        except JWKESTException as e:
            raise AuthTokenError(
                self, ('User info error: Signature verification failed. '
                       'Reason: {0}'.format(e)))
        self.validate_id_token_claims(id_token)
        return id_token
