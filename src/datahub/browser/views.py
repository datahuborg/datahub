import json, sys, re, hashlib, smtplib, base64, urllib, os

from auth import *

from core.handler import DataHubHandler
from datahub import DataHub

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

from thrift.protocol.TJSONProtocol import TJSONProtocol
from thrift.transport import TTransport
from thrift.transport.TTransport import TMemoryBuffer

'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Web Handler
'''

handler = DataHubHandler()
processor = DataHub.Processor(handler)

def home(request):
  try:
    login = get_login(request)
    if login:
      return HttpResponseRedirect('/browse/%s' %(login))
    else:
      return render_to_response("home.html")
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


@login_required
def console(request):
  return render_to_response("console.html", {
    'login': get_login(request)})


@csrf_exempt
def api(request):
  try:
    iprot = TJSONProtocol(
        TMemoryBuffer(request.body))
    oprot = TJSONProtocol(TMemoryBuffer())
    processor.process(iprot, oprot)
    resp = HttpResponse(
        oprot.trans.getvalue(),
        mimetype="application/json")
    resp['Access-Control-Allow-Origin'] = "*"
    return resp
  except Exception, e:
    print str(e)
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


def user(request, username):
  try:
    if(username):
      res = manager.list_repos(username)
      repos = [t[0] for t in res['tuples']]
      return render_to_response("user.html", {
          'login': get_login(request),
          'username': username,
          'repos': repos})      
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

def repo(request, username, repo):
  try:
    res = manager.list_tables(username, repo)
    tables = [t[0] for t in res['tuples']]
    return render_to_response("repo.html", {
        'login': get_login(request),
        'username': username,
        'repo': repo,
        'tables': tables})
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

def table(request, username, repo, table):
  try:
    res = manager.execute_sql(
        username=username,
        query='SELECT * from %s.%s.%s' %(username, repo, table))
    column_names = res['column_names']
    tuples = res['tuples']
    return render_to_response("table.html", {
        'login': get_login(request),
        'username': username,
        'repo': repo,
        'table': table,
        'column_names': column_names,
        'tuples': tuples})
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")



