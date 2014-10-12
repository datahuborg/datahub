import codecs
import collections
import csv
import json
import os
import re
import sys
import urllib

from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.http import *
from django.shortcuts import render_to_response
from django.utils.http import urlquote_plus
from django.views.decorators.csrf import csrf_exempt

from thrift.protocol import TBinaryProtocol
from thrift.protocol import TJSONProtocol
from thrift.transport import TTransport
from thrift.transport.TTransport import TMemoryBuffer

from apps.refiner import inference
from auth import *
from core.handler import DataHubHandler
from core.db.manager import DataHubManager
from datahub import DataHub
from utils import *

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
def files(request, repo_owner, repo):
  repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
  if not os.path.exists(repo_dir):
    os.makedirs(repo_dir)
  
  uploaded_files = [f for f in os.listdir(repo_dir)]
  res= {'login': get_login(request),
        'repo_owner': repo_owner,
        'repo':repo,
        'files': uploaded_files}
  res.update(csrf(request))
  return render_to_response("files.html", res)

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
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

def get_manager(request, repo_owner):
  login = get_login(request)
  manager = DataHubManager(user=login, database=repo_owner)
  return manager

def user(request, repo_owner):
  try:
    manager = get_manager(request, repo_owner)

    res = manager.list_repos()
    repos = [{'name':t[0], 'owner': repo_owner} for t in res['tuples']]

    shared_repos = None
    #res = manager.list_shared_repos(username)
    #shared_repos = [{'name':t[1], 'owner': t[0]} for t in res['tuples']]
    
    return render_to_response("user.html", {
        'login': get_login(request),
        'repo_owner': repo_owner,
        'repos': repos,
        'shared_repos': shared_repos})      
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

def repo(request, repo_owner, repo):
  try:
    manager = get_manager(request, repo_owner)
    
    res = manager.list_tables(repo)
    tables = [t[0] for t in res['tuples']]

    repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
    if not os.path.exists(repo_dir):
      os.makedirs(user_dir)
    
    uploaded_files = [f for f in os.listdir(repo_dir)]
    
    res = {
        'login': get_login(request),
        'repo_owner': repo_owner,
        'repo': repo,
        'tables': tables,
        'files': uploaded_files}
    return render_to_response("repo.html", res)
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

def settings_repo(request, repo_owner, repo):
  try:
    manager = get_manager(request, repo_owner)
    
    res = manager.list_tables(repo)
    tables = [t[0] for t in res['tuples']]
    res = {
        'login': get_login(request),
        'repo_owner': repo_owner,
        'repo': repo,
        'tables': tables}
    return render_to_response("settings_repo.html", res)
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

def table(request, repo_owner, repo, table, page='1'):
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

  end_page = start_page + 10

  try:
    manager = get_manager(request, repo_owner)

    res = manager.execute_sql(
        query='SELECT count(*) from %s.%s.%s' %(repo_owner, repo, table))    
    
    count = res['tuples'][0][0]    
    total_pages = 1 + (int(count) / 50)
    
    if end_page > total_pages:
      end_page = total_pages
      
    res = manager.execute_sql(
        query='SELECT * from %s.%s.%s LIMIT 100 OFFSET %s'
        %(repo_owner, repo, table, (current_page -1) * 100))
    
    column_names = [field['name'] for field in res['fields']]
    tuples = res['tuples']
    return render_to_response("table.html", {
        'login': get_login(request),
        'repo_owner': repo_owner,
        'repo': repo,
        'table': table,
        'column_names': column_names,
        'tuples': tuples,
        'current_page': current_page,
        'pages': range(start_page, end_page)})
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")


def save_uploaded_file(repo_owner, repo, data_file):
  repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
  if not os.path.exists(repo_dir):
    os.makedirs(repo_dir)
  
  file_name = '%s/%s' %(repo_dir, data_file.name)
  with open(file_name, 'wb+') as destination:
    for chunk in data_file.chunks():
      destination.write(chunk)

@login_required
def handle_file_upload(request):
  try:
    if request.method == 'POST':
      data_file = request.FILES['data_file']
      repo = request.POST['repo']
      repo_owner = request.POST['repo_owner']
      save_uploaded_file(repo_owner, repo, data_file)
    
    return HttpResponseRedirect('/files/%s/%s' %(repo_owner, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_import(request, repo_owner, repo):
  try:
    login = get_login(request)
    file_name = request.GET['file']
    repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
    file_path = '%s/%s' %(repo_owner, file_name)
    table_name, _ = os.path.splitext(file_name)
    table_name = clean_str(table_name, 'table')
    dh_table_name = '%s.%s.%s' %(repo_owner, repo, table_name)
    f = codecs.open(file_path, 'r', 'ISO-8859-1')
    data = csv.reader(f)
    cells = data.next()
    columns = map(lambda x: clean_str(x, 'column'), cells)
    columns = rename_duplicates(columns)
    query = 'CREATE TABLE %s (%s text' % (dh_table_name, columns[0])
    for i in range(1, len(columns)):
      query += ', %s %s' %(columns[i], 'text')
    query += ')'
    
    manager = get_manager(request, repo_owner)
    manager.execute_sql(query=query)
    Manager.import_file(path=file_path, table_name=dh_table_name)
    return HttpResponseRedirect('/browse/%s/%s' %(repo_owner, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_delete(request, repo_owner, repo):
  try:
    login = get_login(request)
    file_name = request.GET['file']
    repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
    file_path = '%s/%s' %(repo_dir, file_name)
    os.remove(file_path)
    return HttpResponseRedirect('/browse/%s/%s' %(repo_owner, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def table_delete(request, repo_owner, repo, table_name):
  try:
    manager = get_manager(request, repo_owner)
    
    dh_table_name = '%s.%s.%s' %(repo_owner, repo, table_name)
    query = '''DROP TABLE %s''' %(dh_table_name)
    manager.execute_sql(query=query)
    return HttpResponseRedirect('/browse/%s/%s' %(repo_owner, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_download(request, repo_owner, repo):
  try:
    login = get_login(request)
    file_name = request.GET['file']
    repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
    file_path = '%s/%s' %(repo_dir, file_name)
    response = HttpResponse(
        open(file_path).read(), mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' %(file_name)
    return response
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_export(request, repo_owner, repo, table_name):
  try:
    login = get_login(request)
    repo_dir = '/user_data/%s/%s' %(repo_owner, repo)
    
    if not os.path.exists(user_dir):
      os.makedirs(repo_dir)
    
    file_path = '%s/%s.csv' %(repo_dir, table_name)
    dh_table_name = '%s.%s.%s' %(repo_owner, repo, table_name)
    Manager.export_file(
        repo_owner=repo_owner, path=file_path, table_name=dh_table_name)
    return HttpResponseRedirect('/browse/%s/%s' %(repo_owner, repo))
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
