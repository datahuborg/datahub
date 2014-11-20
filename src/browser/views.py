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

from account.auth import *
from core.db.manager import DataHubManager
from core.handler import DataHubHandler
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
      return HttpResponseRedirect('/www')
  except Exception, e:
    return HttpResponse(
        json.dumps({'error': str(e)}),
        mimetype="application/json")


'''
APIs and Services
'''

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
        json.dumps({'error': str(e)}),
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
        json.dumps({'error': str(e)}),
        mimetype="application/json")


'''
Repository Base
'''

@login_required
def user(request, repo_base):
  try:
    login = get_login(request)

    res = DataHubManager.has_base_privilege(login, repo_base, 'CONNECT')
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')

    manager = DataHubManager(user=repo_base)
    res = manager.list_repos()
    repos = [t[0] for t in res['tuples']]

    visible_repos = []
    
    for repo in repos:
      res = manager.list_collaborators(repo_base, repo)

      collaborators = [(c[0].split('=')[0]).strip() for c in res['tuples']]
      collaborators = filter(lambda x: x!='' and x!=repo_base, collaborators)

      if login not in collaborators and login != repo_base:
        continue

      visible_repos.append({
          'name':repo,
          'owner': repo_base,
          'public': True if 'PUBLIC' in collaborators else False,
          'collaborators': collaborators,
          'collaborators_str': ', '.join(collaborators),
          'num_collaborators': len(collaborators)
      })
    
    return render_to_response("user.html", {
        'login': get_login(request),
        'repo_base': repo_base,
        'repos': visible_repos})    
  
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")


'''
Repository
'''

@login_required
def repo(request, repo_base, repo):
  try:
    login = get_login(request)

    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'USAGE')
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')
    
    manager = DataHubManager(user=repo_base)
    res = manager.list_tables(repo)
    tables = [t[0] for t in res['tuples']]

    repo_dir = '/user_data/%s/%s' %(repo_base, repo)
    if not os.path.exists(repo_dir):
      os.makedirs(repo_dir)
    
    uploaded_files = [f for f in os.listdir(repo_dir)]
    #cards = []
    cards = [c.card_name for c in Card.objects.all().filter(repo_base=repo_base, repo=repo)]
    
    res = {
        'login': get_login(request),
        'repo_base': repo_base,
        'repo': repo,
        'cards': cards,
        'tables': tables,
        'files': uploaded_files}
    res.update(csrf(request))
    return render_to_response("repo.html", res)
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

@login_required
def repo_create(request, repo_base):
  try:
    login = get_login(request)
    if request.method == "POST":
      if login != repo_base:
        raise Exception(
            'Permission denied. '
            '%s can\'t create new repository in %s.' %(login, repo_base))

      repo = request.POST['repo']
      manager = DataHubManager(user=repo_base)
      manager.create_repo(repo)

      return HttpResponseRedirect('/browse/%s' %(repo_base))

    else:
      res = {'repo_base': repo_base, 'login':login}
      res.update(csrf(request))
      return render_to_response("create-repo.html", res)
  
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

@login_required
def repo_delete(request, repo_base, repo):
  try:
    login = get_login(request)

    if login != repo_base:
      raise Exception(
          'Permission denied. '
          '%s can\'t delete repository %s in %s.' %(login, repo, repo_base))

    manager = DataHubManager(user=repo_base)
    manager.delete_repo(repo=repo, force=True)
    return HttpResponseRedirect('/browse/%s' %(repo_base))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def repo_settings(request, repo_base, repo):
  try:
    login = get_login(request)
    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'CREATE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')
    
    manager = DataHubManager(user=repo_base)
    res = manager.list_collaborators(repo_base, repo)
    
    collaborators = [(c[0].split('=')[0]).strip() for c in res['tuples']]
    collaborators = filter(lambda x: x!='' and x!=repo_base, collaborators)

    res = {
        'login': get_login(request),
        'repo_base': repo_base,
        'repo': repo,
        'collaborators': collaborators}
    res.update(csrf(request))
    return render_to_response("repo-settings.html", res)
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

@login_required
def repo_collaborators_add(request, repo_base, repo):
  try:
    login = get_login(request)
    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'CREATE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')
    
    username = request.POST['collaborator_username']
    manager = DataHubManager(user=repo_base)
    manager.add_collaborator(
        repo, username, privileges=['SELECT', 'INSERT', 'UPDATE'])
    return HttpResponseRedirect('/settings/%s/%s' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def repo_collaborators_remove(request, repo_base, repo, username):
  try:
    login = get_login(request)
    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'CREATE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')
    
    manager = DataHubManager(user=repo_base)
    manager.delete_collaborator(repo, username)
    return HttpResponseRedirect('/settings/%s/%s' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


'''
Tables
'''

@login_required
def table(request, repo_base, repo, table):
  try:
    login = get_login(request)
    dh_table_name = '%s.%s.%s' %(repo_base, repo, table)
    
    res = DataHubManager.has_table_privilege(
        login, repo_base, dh_table_name, 'SELECT')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')

    manager = DataHubManager(user=repo_base)
    res = manager.execute_sql(
        query='SELECT count(*) from %s' %(dh_table_name))    
    
    limit = 50
    
    count = res['tuples'][0][0]    
    total_pages = 1 + (int(count) / limit)

    current_page = 1
    try:
      current_page = int(request.REQUEST['page'])
    except:
      pass

    if current_page < 1:
      current_page = 1

    start_page = current_page - 5
    if start_page < 1:
      start_page = 1

    end_page = start_page + 10
    
    if end_page > total_pages:
      end_page = total_pages
      
    res = manager.execute_sql(
        query='SELECT * from %s LIMIT %s OFFSET %s'
        %(dh_table_name, limit, (current_page -1) * limit))
    
    column_names = [field['name'] for field in res['fields']]
    tuples = res['tuples']

    annotation_text = None
    url_path = '/browse/%s/%s/table/%s' %(repo_base, repo, table)
    try:
      annotation = Annotation.objects.get(url_path=url_path)
      annotation_text = annotation.annotation_text
    except:
      pass

    data = {
        'login': get_login(request),
        'repo_base': repo_base,
        'repo': repo,
        'table': table,
        'column_names': column_names,
        'tuples': tuples,
        'annotation': annotation_text,
        'current_page': current_page,
        'next_page': current_page + 1,
        'prev_page': current_page - 1,
        'url_path': url_path,
        'total_pages': total_pages,
        'pages': range(start_page, end_page + 1)}

    data.update(csrf(request))
    return render_to_response("table.html", data)
  except Exception, e:
    return HttpResponse(json.dumps(
        {'error': str(e)}),
        mimetype="application/json")

@login_required
def table_export(request, repo_base, repo, table_name):
  try:
    login = get_login(request)
    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'CREATE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')
    
    repo_dir = '/user_data/%s/%s' %(repo_base, repo)
    
    if not os.path.exists(repo_dir):
      os.makedirs(repo_dir)
    
    file_path = '%s/%s.csv' %(repo_dir, table_name)
    dh_table_name = '%s.%s.%s' %(repo_base, repo, table_name)
    DataHubManager.export_file(
        repo_base=repo_base, table_name=dh_table_name, file_path=file_path)
    return HttpResponseRedirect('/browse/%s/%s#files' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def table_delete(request, repo_base, repo, table_name):
  try:
    login = get_login(request)
    dh_table_name = '%s.%s.%s' %(repo_base, repo, table_name)
    
    res = DataHubManager.has_table_privilege(
        login, repo_base, dh_table_name, 'DELETE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')

    manager = DataHubManager(user=repo_base)
    
    query = '''DROP TABLE %s''' %(dh_table_name)
    manager.execute_sql(query=query)
    return HttpResponseRedirect('/browse/%s/%s' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


'''
Files
'''

def file_save(repo_base, repo, data_file):
  repo_dir = '/user_data/%s/%s' %(repo_base, repo)
  if not os.path.exists(repo_dir):
    os.makedirs(repo_dir)
  
  file_name = '%s/%s' %(repo_dir, data_file.name)
  with open(file_name, 'wb+') as destination:
    for chunk in data_file.chunks():
      destination.write(chunk)

@login_required
def file_upload(request, repo_base, repo):
  try:    
    data_file = request.FILES['data_file']
    file_save(repo_base, repo, data_file)    
    return HttpResponseRedirect('/browse/%s/%s#files' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_import(request, repo_base, repo, file_name):
  try:
    login = get_login(request)
    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'CREATE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')
    
    delimiter = str(request.GET['delimiter'])    
    if delimiter == '':
      delimiter = str(request.GET['other_delimiter'])
    
    header = True if request.GET['has_header'] == "true" else False
    
    quote_character = request.GET['quote_character']
    if quote_character == '':
      quote_character = request.GET['other_quote_character']

    delimiter = delimiter.decode('string_escape')
    
    repo_dir = '/user_data/%s/%s' %(repo_base, repo)
    file_path = '%s/%s' %(repo_dir, file_name)
    table_name, _ = os.path.splitext(file_name)
    table_name = clean_str(table_name, 'table')
    dh_table_name = '%s.%s.%s' %(repo_base, repo, table_name)

    f = codecs.open(file_path, 'r', 'ISO-8859-1')

    data = csv.reader(f, delimiter=delimiter)
    cells = data.next()
    
    columns = [clean_str(str(i), 'col') for i in range(0, len(cells))]
    if header:
      columns = map(lambda x: clean_str(x, 'col'), cells)
    
    columns = rename_duplicates(columns)
    
    query = 'CREATE TABLE %s (%s text' % (dh_table_name, columns[0])

    for i in range(1, len(columns)):
      query += ', %s %s' %(columns[i], 'text')
    query += ')'
    
    manager = DataHubManager(user=repo_base)
    manager.execute_sql(query=query)
    manager.import_file(
        repo_base=repo_base,
        table_name=dh_table_name,
        file_path=file_path,
        delimiter=delimiter,
        header=header,
        quote_character=quote_character)
    return HttpResponseRedirect('/browse/%s/%s' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_delete(request, repo_base, repo, file_name):
  try:
    login = get_login(request)
    res = DataHubManager.has_repo_privilege(login, repo_base, repo, 'CREATE')
    
    if not (res and res['tuples'][0][0]):
      raise Exception('Access denied. Missing required privileges.')

    repo_dir = '/user_data/%s/%s' %(repo_base, repo)
    file_path = '%s/%s' %(repo_dir, file_name)
    os.remove(file_path)
    return HttpResponseRedirect('/browse/%s/%s#files' %(repo_base, repo))
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def file_download(request, repo_base, repo, file_name):
  try:
    repo_dir = '/user_data/%s/%s' %(repo_base, repo)
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


'''
Query 
'''
@login_required
def query(request, repo_base, repo):
  try:
    login = get_login(request)
    data = {
        'login': get_login(request),
        'repo_base': repo_base,
        'repo': repo,
        'query': None}
    
    if 'q' in request.REQUEST:
      query = request.REQUEST['q']    
    
      manager = DataHubManager(user=repo_base)
      res = manager.execute_sql(
          query='EXPLAIN %s' %(query))    
      
      limit = 50
      
      num_rows = re.match(r'.*rows=(\d+).*', res['tuples'][0][0]).group(1)
      count = int(num_rows)    
      total_pages = 1 + (int(count) / limit)

      current_page = 1
      try:
        current_page = int(request.REQUEST['page'])
      except:
        pass

      if current_page < 1:
        current_page = 1

      start_page = current_page - 5
      if start_page < 1:
        start_page = 1

      end_page = start_page + 10
      
      if end_page > total_pages:
        end_page = total_pages
        
      res = manager.execute_sql(
          query='%s LIMIT %s OFFSET %s'
          %(query, limit, (current_page -1) * limit))
      
      column_names = [field['name'] for field in res['fields']]
      tuples = res['tuples']

      url_path = '/browse/%s/%s/query' %(repo_base, repo)

      data.update({
          'query': query,
          'column_names': column_names,
          'tuples': tuples,
          'url_path': url_path,
          'current_page': current_page,
          'next_page': current_page + 1,
          'prev_page': current_page - 1,
          'total_pages': total_pages,
          'pages': range(start_page, end_page + 1)})

    data.update(csrf(request))
    return render_to_response("query.html", data)
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


'''
Annotations
'''

@login_required
def create_annotation(request):
  try:    
    url = request.POST['url']
    annotation_text = request.POST['annotation']
    
    try:
      annotation = Annotation.objects.get(url_path=url)
      annotation.annotation_text = annotation_text
      annotation.save()
    except Annotation.DoesNotExist:
      annotation = Annotation(
          url_path=url, annotation_text=annotation_text)
      annotation.save()
    
    return HttpResponseRedirect(url)
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")


'''
Cards
'''

@login_required
def card(request, repo_base, repo, card):
  try:
    login = get_login(request)
    card = Card.objects.get(repo_base=repo_base, repo=repo, card_name=card_name)
    query = card.query  
    manager = DataHubManager(user=repo_base)
    res = manager.execute_sql(
        query='EXPLAIN %s' %(query))    
    
    limit = 50
    
    num_rows = re.match(r'.*rows=(\d+).*', res['tuples'][0][0]).group(1)
    count = int(num_rows)    
    total_pages = 1 + (int(count) / limit)

    current_page = 1
    try:
      current_page = int(request.REQUEST['page'])
    except:
      pass

    if current_page < 1:
      current_page = 1

    start_page = current_page - 5
    if start_page < 1:
      start_page = 1

    end_page = start_page + 10
    
    if end_page > total_pages:
      end_page = total_pages
      
    res = manager.execute_sql(
        query='%s LIMIT %s OFFSET %s'
        %(query, limit, (current_page -1) * limit))
    
    column_names = [field['name'] for field in res['fields']]
    tuples = res['tuples']

    url_path = '/browse/%s/%s/card/%s' %(repo_base, repo, card_name)

    data.update({
        'card_name': card_name,
        'query': query,
        'column_names': column_names,
        'tuples': tuples,
        'url_path': url_path,
        'current_page': current_page,
        'next_page': current_page + 1,
        'prev_page': current_page - 1,
        'total_pages': total_pages,
        'pages': range(start_page, end_page + 1)})

    data.update(csrf(request))
    return render_to_response("query.html", data)    
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")

@login_required
def create_card(request, repo_base, repo):
  try:    
    card_name = request.POST['card_name']
    query = request.POST['query']
    url = '/browse/%s/%s/card/%s' %(repo_base, repo, card_name)

    card = Card(
        repo_base=repo_base, repo=repo, card_name=card_name, query=Query)
    card.save()    
    return HttpResponseRedirect(url)
  except Exception, e:
    return HttpResponse(
        json.dumps(
          {'error': str(e)}),
        mimetype="application/json")