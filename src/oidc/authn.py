from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseBadRequest

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.oic.message import RegistrationResponse
from oic.oic.message import AuthorizationResponse
from oic.oauth2 import rndstr
from oic.exception import PyoidcError

import re

# This configuration info only works if you use the domain name
# datahub-local.mit.edu. If you want to use something different,
# you can register your own OIDC client with MIT's server at
# https://oidc.mit.edu/manage/dev/dynreg/new and with Google at
# https://console.developers.google.com. Instructions for
# Google are available at
# https://developers.google.com/identity/protocols/OpenIDConnect.

OIDC_CLIENT_CONFIG = {
    'mit': {
        'discovery_url': "https://oidc.mit.edu/",
        'user_info_request_method': 'POST',
        'redirect_uris': ["https://datahub-local.mit.edu/oidc/redirect"],
        'client_info': {
            "client_id": "4ca40749-0167-42f9-93ef-3fe01913e286",
            "client_secret": "ALdm9d_rnG9RPkvhS5wMTqlRdpwaEstxhI_b5n2PP-3zaF5piPlF-n23jOzDfg0eN5gskeIHrK5595zZEuifKYA"
        }
    },
    'google': {
        'discovery_url': "https://accounts.google.com/",
        'user_info_request_method': 'GET', # Google's user_info_endpoint only supports GET
        'redirect_uris': ["https://datahub-local.mit.edu/oidc/redirect"],
        'client_info': {
            "client_id": "709052285863-3nd6f2cb168iavlc7n47v92jqnioib5a.apps.googleusercontent.com",
            "client_secret": "JGdH-6svbSnypuIccfeoNXwt"
        }
    }
}

class OIDCError(Exception):
    def __init__(self, errmsg, message="", *args):
        Exception.__init__(self, errmsg, *args)
        self.message = message

def build_client(provider):
    if provider not in OIDC_CLIENT_CONFIG:
        raise OIDCError("Unknown provider.")

    config = OIDC_CLIENT_CONFIG[provider]
    client_info = config['client_info']

    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    client.provider_config(config["discovery_url"])
    client.redirect_uris = config["redirect_uris"]

    client_reg = RegistrationResponse(**client_info)
    client.client_info = client_reg
    client.client_id = client_info["client_id"]
    client.client_secret = client_info["client_secret"]

    return client


def provider_login(request):
    if 'provider' in request.GET and len(request.GET['provider']) > 0:
        provider = request.GET['provider']
    else:
        return HttpResponseBadRequest("Missing provider query parameter.")

    if 'target' in request.GET and len(request.GET['target']) > 0:
        request.session['target'] = request.GET['target']
    elif 'HTTP_REFERER' in request.META:
        request.session['target'] = request.META['HTTP_REFERER']

    client = build_client(provider)

    request.session['provider'] = provider
    request.session['state'] = rndstr()
    request.session['nonce'] = rndstr()

    args = {
        "client_id": client.client_id,
        "response_type": "code",
        "scope": ["openid", "email", "profile"],
        "state": request.session['state'],
        "nonce": request.session['nonce'],
        "redirect_uri": client.redirect_uris[0]
    }
    authz_req = client.construct_AuthorizationRequest(request_args=args)
    login_url = authz_req.request(client.authorization_endpoint)

    return HttpResponseRedirect(login_url)


def provider_callback(request):
    provider = request.session['provider']
    client = build_client(provider)

    response = request.META["QUERY_STRING"]

    aresp = client.parse_response(AuthorizationResponse, info=response, sformat="urlencoded")

    # Make sure this is a callback we're expecting.
    received_state = aresp['state']
    if 'state' not in request.session or request.session['state'] != received_state:
        return HttpResponseBadRequest("States didn't match.")
    del request.session['state']

    args = {
        "code": aresp["code"],
        "redirect_uri": client.redirect_uris[0],
        "client_id": client.client_id,
        "client_secret": client.client_secret
    }

    atresp = client.do_access_token_request(scope="openid",
                                            state=received_state,
                                            request_args=args,
                                            authn_method="client_secret_basic"
                                            )

    # Save provider's OAuth access token for later
    access_token = atresp['access_token']
    request.session['access_token'] = access_token

    if 'target' in request.session:
        target = request.session['target']
        target = re.sub(r"^http:", "https:", target)
        del request.session['target']
    else:
        target = 'https://' + request.META['HTTP_HOST']

    return HttpResponseRedirect(target)

def logout(request):
    request.session.flush()

    if 'HTTP_REFERER' in request.META:
        target = request.META['HTTP_REFERER']
    else:
        target = 'https://' + request.META['HTTP_HOST']

    target = re.sub(r"^http:", "https:", target)
    return HttpResponseRedirect(target)

def oidc_user_info(request):
    try:
        access_token = request.session['access_token']
        provider = request.session['provider']
        request_method = OIDC_CLIENT_CONFIG[provider]['user_info_request_method']
        client = build_client(provider)
        user_info = client.do_user_info_request(method=request_method, access_token=access_token)
        result = user_info.to_dict()
        result['issuer'] = client.provider_info['issuer']
        if 'preferred_username' in result:
            result['username'] = result['preferred_username']
        result['access_token'] = access_token
    except KeyError as error:
        result = { "debug": str(error) + " not found." }
    except PyoidcError:
        result = { "error": "PyoidcError", "provider": provider }

    return result
