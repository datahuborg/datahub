import json, sys, re, hashlib, smtplib, base64, urllib, os, csv, collections, codecs

from auth import *

from core.handler import DataHubHandler
from apps.refiner import inference
from datahub import DataHub

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

from thrift.protocol import TBinaryProtocol
from thrift.protocol import TJSONProtocol
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

@login_required
def newtable(request, username, repo):
  res= {'login': get_login(request), 'username': get_login(request), 'repo':repo}
  res.update(csrf(request))
  return render_to_response("newtable.html", res)

@login_required
def data_refiner(request):
  return render_to_response("data-refiner.html", {
    'login': get_login(request)})

@csrf_exempt
def service_binary(request):
  try:
    iprot = TBinaryProtocol.TBinaryProtocol(TMemoryBuffer(request.body))
    oprot = TBinaryProtocol.TBinaryProtocol(TMemoryBuffer())
    processor.process(iprot, oprot)
    resp = HttpResponse(oprot.trans.getvalue())
    resp['Access-Control-Allow-Origin'] = "*"
    return resp
  except Exception, e:
    print str(e)
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@csrf_exempt
def service_json(request):
  try:
    iprot = TJSONProtocol.TJSONProtocol(TMemoryBuffer(request.body))
    oprot = TJSONProtocol.TJSONProtocol(TMemoryBuffer())
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
    return render_to_response("repo.html", res)
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

def table(request, username, repo, table, page='1'):
  current_page = 1
  try:
    current_page = int(page)
  except:
    pass

  if current_page < 1:
      current_page = 1

  start_page = current_page - 5
  if start_page < 1:
    start_page = 1

  try:
    res = manager.execute_sql(
        username=username,
        query='SELECT count(*) from %s.%s.%s' %(username, repo, table))
    count = res['tuples'][0][0]
    total_pages = 1 + (int(count) / 100)
    end_page = start_page + 10
    if end_page > total_pages:
      end_page = total_pages
      
    res = manager.execute_sql(
        username=username,
        query='SELECT * from %s.%s.%s LIMIT 100 OFFSET %s' %(username, repo, table, (current_page -1) * 100))
    column_names = [field['name'] for field in res['fields']]
    tuples = res['tuples']
    return render_to_response("table.html", {
        'login': get_login(request),
        'username': username,
        'repo': repo,
        'table': table,
        'column_names': column_names,
        'tuples': tuples,
        'current_page': current_page,
        'pages': range(start_page, end_page)})
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


def handle_uploaded_file(file_name, file_data):
  with open(file_name, 'wb+') as destination:
    for chunk in file_data.chunks():
      destination.write(chunk)

def save_uploaded_file(file_name, file_data):
  f = open(file_name, 'wb+')
  f.write(file_data)

@login_required
def create_table_from_file(request):
  try:
    login = get_login(request)
    repo = ''
    if request.method == 'POST':
      file_data = request.FILES['data_file']
      table_name = request.POST['table_name']
      repo = request.POST['repo']
      file_name = '/tmp/%s_%s_%s.csv' %(login, repo, table_name)
      dh_table_name = '%s.%s.%s' %(login, repo, table_name)
      handle_uploaded_file(file_name, file_data)
      f = codecs.open(file_name, 'r', 'utf-8')
      data = csv.reader(f)
      cells = data.next()
      columns = map(lambda x: re.sub(r'\W+', '_', x), cells)
      columns = map(lambda x: re.sub(r'\.', '_', x), columns)
      columns = map(lambda x: '_' + x[-20:], columns)
      columns = filter(lambda x: x!='', columns)
      query = 'CREATE TABLE %s (%s text' % (dh_table_name, columns[0])
      for i in range(1, len(columns)):
        query += ', %s %s' %(columns[i], 'text')
      query += ')'
      manager.execute_sql(
        username=login, query=query)
      manager.create_table_from_file(path=file_name, database=login, table_name=dh_table_name)

    return HttpResponseRedirect('/browse/%s/%s' %(login, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@csrf_exempt
@login_required
def create_table_from_file_data(request):
  try:
    login = get_login(request)
    repo = ''
    if request.method == 'POST':
      file_data = request.POST['data']
      table_name = request.POST['table_name']
      repo = request.POST['repo']
      file_name = '/tmp/%s_%s_%s.csv' %(login, repo, table_name)
      dh_table_name = '%s.%s.%s' %(login, repo, table_name)
      save_uploaded_file(file_name, file_data)
      f = codecs.open(file_name, 'r', 'utf-8')
      data = csv.reader(f)
      cells = data.next()
      columns = []
      i = 1
      for cell in cells:
        columns.append('col_%s' %(i))
        i += 1

      query = 'CREATE TABLE %s (%s text' % (dh_table_name, columns[0])
      for i in range(1, len(columns)):
        query += ', %s %s' %(columns[i], 'text')
      query += ')'
      manager.execute_sql(
        username=login, query=query)
      manager.create_table_from_file(path=file_name, database=login, table_name=dh_table_name)

    return HttpResponseRedirect('/browse/%s/%s' %(login, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")



@csrf_exempt
def refine_data(request):
  res  = {'error': None}
  try:
    if request.method == 'POST':
      training_input = request.POST['training_input']
      training_output = request.POST['training_output']
      test_data = request.POST['test_data']
      record_separator = '\n'
      if 'record_separator' in request.POST:
        record_separator = request.POST['record_separator']

      o_fields_structure, i_structure = inference.learn_mapping(training_input, training_output)
      out = inference.extract(test_data, o_fields_structure, sep=record_separator)

      csv_lines = []
      for row in out:
        csv_lines.append(','.join(row.values()))

      csv_str = '\n'.join(csv_lines)
      res['output'] = csv_str
    else:
      res['error'] = 'Invalid HTTP Method'      
  except Exception, e:
    res['error'] = str(e)

  return HttpResponse(json.dumps(res), mimetype="application/json")
