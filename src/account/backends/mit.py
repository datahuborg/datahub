from social.backends.open_id import OpenIdConnectAuth, OpenIdConnectAssociation
from jwt import InvalidTokenError, decode as jwt_decode
from social.exceptions import AuthTokenError

class MITOpenIdConnect(OpenIdConnectAuth):
    name = 'mit-oidc'

    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'sub'
    AUTHORIZATION_URL = 'https://oidc.mit.edu/authorize'
    ACCESS_TOKEN_URL = 'https://oidc.mit.edu/token'
    USER_INFO_URL = 'https://oidc.mit.edu/userinfo'

    DEFAULT_SCOPE = ['openid', 'email', 'profile']

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
            return self.strategy.storage.association.get(
                server_url=self.AUTHORIZATION_URL,
                handle=nonce
            )[0]
        except IndexError:
            pass

    def user_data(self, access_token, *args, **kwargs):
        response = self.request(self.USER_INFO_URL,
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

    def validate_and_return_id_token(self, id_token):
        """
        Validates the id_token according to the steps at
        http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation.
        """
        client_id, _client_secret = self.get_key_and_secret()
        decryption_key = self.setting('ID_TOKEN_DECRYPTION_KEY')
        try:
            # Decode the JWT and raise an error if the secret is invalid or
            # the response has expired.
            print(id_token)
            id_token = jwt_decode(id_token, decryption_key, audience=client_id,
                                  issuer=self.ID_TOKEN_ISSUER,
                                  leeway=3000,
                                  algorithms=['HS256'])
        except InvalidTokenError as err:
            raise AuthTokenError(self, err)

        # Validate the nonce to ensure the request was not modified
        nonce = id_token.get('nonce')
        if not nonce:
            raise AuthTokenError(self, 'Incorrect id_token: nonce')

        print("nonce: {0}".format(nonce))

        nonce_obj = self.get_nonce(nonce)
        print("nonce_obj: {0}".format(nonce_obj))
        if nonce_obj:
            self.remove_nonce(nonce_obj.id)
        else:
            raise AuthTokenError(self, 'Incorrect id_token: nonce')
        return id_token
