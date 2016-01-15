from django.shortcuts import render_to_response
from django.http import HttpResponse
import json

'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Console
'''


def index(request):
    try:
        c = {'login': request.user.get_username()}
        return render_to_response("index.html", c)
    except Exception as e:
        return HttpResponse(
            json.dumps({'error': str(e)}),
            content_type="application/json")
