from django.shortcuts import render_to_response

from account.auth import *


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Console
'''

@login_required
def index(request):
  return render_to_response("console.html", {
    'login': get_login(request)})