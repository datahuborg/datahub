from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponsePermanentRedirect
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


def decibel(request):
    """
    The paper, "Decibel: The Relational Dataset Branching System"
    directs readers here for the benchmarking software.

    Redirects people to the repo where that's stored.
    """
    return HttpResponsePermanentRedirect(
        'https://github.com/CSAIL-LivingLab/benchmark')
