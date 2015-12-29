from account.backends.oidc import DataHubFixedOpenIdConnect


class MITOpenIdConnect(DataHubFixedOpenIdConnect):

    """
    PSA backend for MIT's OpenID Connect server at oidc.mit.edu.

    Allows anyone with an @mit.edu email address to log in.
    """

    name = 'mit-oidc'

    OIDC_URL = 'https://oidc.mit.edu'
    RESPONSE_TYPE = 'code'
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    ID_KEY = 'sub'
    USERNAME_KEY = 'preferred_username'
    DEFAULT_SCOPE = ['openid', 'email', 'profile']
