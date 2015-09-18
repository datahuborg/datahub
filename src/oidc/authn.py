from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, HttpResponseBadRequest

from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from oic.oic.message import RegistrationResponse
from oic.oic.message import AuthorizationResponse
from oic.oauth2 import rndstr
from oic.exception import PyoidcError

import re


def build_client(email):
    client = Client(client_authn_method=CLIENT_AUTHN_METHOD)
    uid = email  # "jander@oidc.mit.edu"  # Can't use @mit.edu because web.mit.edu seems to have a bad certificate chain.
    issuer = client.discover(uid)  # Need the MIT CA installed in a place OpenSSL can reach or this will fail.
    client.provider_config(issuer)
    client.redirect_uris = ["https://datahub-local.mit.edu/oidc/redirect"]

    info = {"client_id": "4ca40749-0167-42f9-93ef-3fe01913e286", "client_secret": "ALdm9d_rnG9RPkvhS5wMTqlRdpwaEstxhI_b5n2PP-3zaF5piPlF-n23jOzDfg0eN5gskeIHrK5595zZEuifKYA"}
    client_reg = RegistrationResponse(**info)

    client.client_info = client_reg
    client.client_id = info["client_id"]
    client.client_secret = info["client_secret"]
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

    # Webfinger returns a 404 if you don't provide a real username. This should be redone to be more like the rp3 example, with provider config done in a settings file instead of grabbing it dynamically.
    if provider == 'mit':
        provider = 'jander@oidc.mit.edu'
    elif provider == 'google':
        provider = 'something@accounts.google.com'
    else:
        return HttpResponseBadRequest("Unsupported provider.")

    client = build_client(provider)

    request.session['provider'] = provider
    request.session['state'] = rndstr()
    request.session['nonce'] = rndstr()

    args = {
        "client_id": "4ca40749-0167-42f9-93ef-3fe01913e286",
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

    # Save OAuth access token for later
    # return HttpResponse("Will redirect to \"{0}\"".format(target))

    access_token = atresp['access_token']
    request.session['access_token'] = access_token

    if 'target' in request.session:
        target = request.session['target']
        target = re.sub(r"^http:", "https:", target)
        del request.session['target']
    else:
        target = request.META['HTTP_HOST']

    return HttpResponseRedirect(target)

    # return HttpResponse(user_info.to_json())


def oidc_user_info(request):
    if 'access_token' not in request.session:
        return None
    access_token = request.session['access_token']

    try:
        provider = request.session['provider']
        client = build_client(provider)
        user_info = client.do_user_info_request(access_token=access_token)
        user_info = user_info.to_dict()
        user_info['username'] = user_info['preferred_username']
    except PyoidcError:
        user_info = {}

    return user_info
