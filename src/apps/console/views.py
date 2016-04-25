import json

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

import sys


@login_required
def index(request):
    testing = json.dumps('test' in sys.argv)
    res = {'login': request.user.get_username(), 'testing': testing}
    return render_to_response("console.html", res)
