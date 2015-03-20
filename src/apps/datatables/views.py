import json
from django.shortcuts import render
from django.http import HttpResponse

from core.db.manager import DataHubManager
from account.auth import *

from models.draw_request import DrawRequest

def table(request, table):
    print DrawRequest(request)
    return HttpResponse(json.dumps({"success": True}), content_type="application/json")

