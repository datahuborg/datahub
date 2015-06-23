from django.shortcuts import render_to_response

from account.auth import *


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Console
'''

def index(request):
  try:
    c = {'login': get_login(request)} 
    return render_to_response("index.html", c)
  except Exception, e:
    return HttpResponse(
        json.dumps({'error': str(e)}),
        content_type="application/json")

def developer_apis(request):
  ''' currently not functioning, since layout.html files link
      directly to the static thrift files'''
  try:
    c = {'login': get_login(request)} 
    return render_to_response("apis.html", c)
  except Exception, e:
    return HttpResponse(
        json.dumps({'error': str(e)}),
        content_type="application/json")