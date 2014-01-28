import json, sys, re, hashlib, smtplib, base64, urllib, os, csv, collections

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

@login_required
def visualize(request):
  return render_to_response("visualize.html", {
    'login': get_login(request)})

@login_required
def newrepo(request):
  return render_to_response("newrepo.html", {
    'login': get_login(request)})


@csrf_exempt
def service(request):
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
    res = {
        'login': get_login(request),
        'username': username,
        'repo': repo,
        'tables': tables}
    res.update(csrf(request))
    return render_to_response("repo.html", res)
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


def handle_uploaded_file(username, repo, table_name, file_data):
  file_name, file_extension = os.path.splitext(str(file_data))
  with open('%s/%s/%s.%s' %(username, repo, table_name, file_extension), 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)

def create_table_from_file(request):
  login = get_login(request)
  repo = ''
  if request.method == 'POST':
    data_file = request.FILES['data_file']
    file_extension = os.path.splitext(str(data_file))[1]
    data = csv.DictReader(data_file)
    table_name = request.POST['table_name']
    repo = request.POST['repo']
    columns = map(lambda x: re.sub(r'\W+', '_', x), data.fieldnames)
    dh_table_name = '%s.%s.%s' %(login, repo, table_name)
    query = 'CREATE TABLE %s (%s text' % (dh_table_name, columns[0])
    for i in range(1, len(columns)):
      query += ', %s %s' %(columns[i], 'text')

    query += ')'
    try:
      res = manager.execute_sql(username=login, query=query)
    except Exception, e:
      pass 

    Tuples = collections.namedtuple('Tuples', columns)
    tuples = [Tuples(**row) for row in data]
    
    for t in tuples:
      try:
        query = "INSERT INTO %s (%s) values (%s)" %(dh_table_name, ', '.join(columns), ', '.join(map(lambda x: "'" + x + "'", list(t))))
        manager.execute_sql(username=login, query=query)
      except Exception, e:
        pass



  return HttpResponseRedirect('/browse/%s/%s' %(login, repo))



