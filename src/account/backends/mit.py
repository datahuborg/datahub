from social.backends.open_id import OpenIdConnectAuth, OpenIdConnectAssociation
from jwt import InvalidTokenError, decode as jwt_decode
from social.exceptions import AuthTokenError

import six
import time

from jwkest import JWKESTException
from jwkest.jwk import KEYS
from jwkest.jws import JWS

# Most of this comes from https://github.com/omab/python-social-auth/pull/747,
# an unmerged pull request on Python Social Auth.
#
# PSA 0.2.13's OIDC support is very specific to Google's OIDC server. It only
# supports HS256 signed tokens, doesn't handle signed userinfo responses, and
# doesn't handle situations where the OIDC server's clock is ahead of the
# client's.

class _cache(object):

    """
    Caches method return values for a specific length of time.

    It maintains a cache per class, so subclasses have a different cache entry
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


class MITOpenIdConnect(OpenIdConnectAuth):
    name = 'mit-oidc'

    OIDC_URL = 'https://oidc.mit.edu'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'sub'

    DEFAULT_SCOPE = ['openid', 'email', 'profile']

    @_cache(ttl=86400)
    def oidc_config(self):
        print("Fetching oidc config...")
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
        keys = KEYS()
        keys.load_from_url(self.JWKS_URI)

        # Add client secret as oct key so it can be used for HMAC signatures
        _client_id, client_secret = self.get_key_and_secret()
        keys.add({'key': client_secret, 'kty': 'oct'})
        return keys

    def get_and_store_nonce(self, url, state):
        # Create a nonce
        nonce = self.strategy.random_string(64)
        print("Created nonce {0} for url {1}".format(nonce, url))
        # Store the nonce
        association = OpenIdConnectAssociation(nonce, assoc_type=state)
        self.strategy.storage.association.store(url, association)
        return nonce

    def get_nonce(self, nonce):
        try:
            # PSA 0.2.13 checks the nonce against the ACCESS_TOKEN_URL, but
            # that's the wrong nonce to check.
            return self.strategy.storage.association.get(
                server_url=self.AUTHORIZATION_URL,
                handle=nonce
            )[0]
        except IndexError:
            pass

    def user_data(self, access_token, *args, **kwargs):
        response = self.request(self.USERINFO_URL,
                                headers={'Authorization':
                                         'Bearer {0}'.format(access_token)})
        data = response.content
        client_id, _client_secret = self.get_key_and_secret()
        decryption_key = self.setting('ID_TOKEN_DECRYPTION_KEY')
        try:
            user_info = jwt_decode(data, decryption_key, audience=client_id,
                                   issuer=self.ID_TOKEN_ISSUER,
                                   leeway=3000,
                                   algorithms=['HS256'])
        except InvalidTokenError as err:
            raise AuthTokenError(self, err)

        return user_info

    def get_user_details(self, response):
        return {
            'username': response.get('preferred_username'),
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
            # Decode the JWT and raise an error if the sig is invalid
            id_token = JWS().verify_compact(jws.encode('utf-8'),
                                            self.get_jwks_keys())
        except JWKESTException:
            raise AuthTokenError(self,
                                 'Token error: Signature verification failed')
        # self.validate_claims(id_token)
        return id_token

    # def validate_and_return_id_token(self, id_token):
    #     """
    #     Validates the id_token according to the steps at
    #     http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation.
    #     """
    #     client_id, _client_secret = self.get_key_and_secret()
    #     decryption_key = self.setting('ID_TOKEN_DECRYPTION_KEY')
    #     try:
    #         # Decode the JWT and raise an error if the secret is invalid or
    #         # the response has expired.
    #         print(id_token)
    #         id_token = jwt_decode(id_token, decryption_key, audience=client_id,
    #                               issuer=self.ID_TOKEN_ISSUER,
    #                               leeway=3000,
    #                               algorithms=['HS256'])
    #     except InvalidTokenError as err:
    #         raise AuthTokenError(self, err)

    #     # Validate the nonce to ensure the request was not modified
    #     nonce = id_token.get('nonce')
    #     if not nonce:
    #         raise AuthTokenError(self, 'Incorrect id_token: nonce')

    #     print("nonce: {0}".format(nonce))

    #     nonce_obj = self.get_nonce(nonce)
    #     print("nonce_obj: {0}".format(nonce_obj))
    #     if nonce_obj:
    #         self.remove_nonce(nonce_obj.id)
    #     else:
    #         raise AuthTokenError(self, 'Incorrect id_token: nonce')
    #     return id_token
