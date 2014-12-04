from django.shortcuts import render_to_response

from account.auth import *


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Viz
'''

@login_required
def index(request):
  login = get_login(request)
  return render_to_response("viz.html", {
      'login': login,
      'repo_base': login
  })