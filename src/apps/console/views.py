from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from config.settings import OAUTH2_APP_CLIENTS
import sys


@login_required
def index(request):
    transfer_protocol = 'https://'
    if 'test' in sys.argv:
        transfer_protocol = 'http://'

    res = {'login': request.user.get_username(),
           'transfer_protocol': transfer_protocol,
           'client_id': OAUTH2_APP_CLIENTS['console']['client_id']
           }
    return render_to_response("console.html", res)
