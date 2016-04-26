import json

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from config.settings import OAUTH2_APP_CLIENTS
import sys


@login_required
def index(request):
    testing = json.dumps('test' in sys.argv)
    res = {'login': request.user.get_username(),
              'testing': testing,
              'client_id': OAUTH2_APP_CLIENTS['console']['client_id']
              }
    return render_to_response("console.html", res)
