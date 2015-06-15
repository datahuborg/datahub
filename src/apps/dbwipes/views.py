import json, sys, re, hashlib, smtplib, base64, urllib, os, csv, collections, codecs
import os
import re
import time
import json
import md5
import pdb
import random
import psycopg2
import traceback
import numpy as np

from django.db import connection

from core.db.manager import DataHubManager
from service.handler import DataHubHandler
from datahub import DataHub

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

from thrift.protocol import TBinaryProtocol
from thrift.protocol import TJSONProtocol
from thrift.transport import TTransport
from thrift.transport.TTransport import TMemoryBuffer

from functools import wraps
from collections import *
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.pool import NullPool


from summary import Summary
from util import *

handler = DataHubHandler()
processor = DataHub.Processor(handler)




def returns_json(f):
  @wraps(f)
  def json_returner(*args, **kwargs):
    r = f(*args, **kwargs)
    if not isinstance(r, basestring):
      r = json.dumps(r, cls=SummaryEncoder)
    return HttpResponse(r, content_type='application/json')
  return json_returner


def index(request, username, repo, table):
  if has_scorpion():
    enable_scorpion = 1
    title = 'DBWipes + Scorpion!'
  else:
    enable_scorpion = 0
    title = 'DBWipes'

  schema = get_schema(repo, table, username)
  # pick the first number as y, and first non y as x
  x = y = ''
  for col, typ in schema.iteritems():
    if typ == 'num':
      y = col
      break

  for col, typ in schema.iteritems():
    if col != y and typ in ('str', 'text'):
      x = col
      break

  if x == '':
    for col, typ in schema.iteritems():
      if col != y:
        x = col

  context = {
    'enableScorpion': enable_scorpion,
    'js': 'summary',
    'study': 0,
    'title': title,
    'db': repo,
    'table': table,
    'username': username,
    'repo': repo,
    'x': x,
    'y': y
  }
  return render_to_response("index_base.html", context)

def has_scorpion():
  try:
    import scorpion
    return True
  except:
    return False

@returns_json
def dbs(request):
  username = get_login(request)
  manager = DataHubManager(user=username)
  dbnames = pick(manager.list_repos()['tuples'], 0)
  #q = "SELECT datname FROM pg_database where datistemplate = false;"
  #dbnames = [str(row[0]) for row in manager.execute_sql(query=q)['tuples']]
  return {'databases': dbnames}



@returns_json
def tables(request):
  username = get_login(request)
  manager = DataHubManager(user=username)
  repo = request.GET.get('repo')
  tables = [str(row[0]) for row in manager.list_tables(repo)['tuples']]
  return {'tables': tables}



def get_schema(repo, table, username):
  full_tablename = "%s.%s" % (repo, table)
  manager = DataHubManager(user=username)
  pairs = manager.get_schema(full_tablename)['tuples']
  schema = {}
  for col, typ in pairs:
    if typ == 'text':
      typ = 'str'
    if 'double' in typ:
      typ = 'num'
    if 'int' in typ:
      typ = 'num'
    if 'date' in typ or 'time' in typ:
      typ = 'time'
    schema[str(col)] = str(typ)
  return schema



@returns_json
def schema(request):
  username = request.GET.get('username', '')
  table = request.GET.get('table', '')
  db = request.GET.get('db', '')
  if not table:
    return {}

  ret = {}
  ret['schema'] = get_schema(db, table, username)
  return ret


@returns_json
def requestid(request):
  if not has_scorpion():
    return {'error': "Scorpion not installed"}

  from scorpion.util import Status
  status = Status()
  requestid = status.reqid
  status.close()
  print "requestid", requestid
  return {'requestid': requestid}


@returns_json
def api_status(request):
  if not has_scorpion():
    return {'error': "Scorpion not installed"}

  from scorpion.util import Status
  rid = int(request.GET.get('requestid'))

  status = Status(rid)
  ret = status.latest_status()
  label_rules = status.get_rules()
  status.close()

  partial_rules = []
  for label, rules in label_rules:
    partial_rules.extend(rules)
  rules_hash = hash(str(partial_rules))

  return {
    'status': ret,
    'results': partial_rules,
    'hash': rules_hash
  }


@returns_json
def api_tuples(request):
  ret = { }
  jsonstr = request.GET.get('json')
  if not jsonstr:
    print "query: no json string.  giving up"
    return ret

  args = json.loads(jsonstr)
  username = args.get('username')
  dbname = repo = args.get('db')
  table = args.get('table')
  where = args.get('where', []) or []
  full_tablename = "%s.%s" % (dbname, table)

  where, params = where_to_sql(where)
  if where:
    where = 'AND %s' % where
  print where
  print params

  query = """WITH XXXX as (select count(*) from %s WHERE 1 = 1 %s)
  SELECT * FROM %s 
  WHERE random() <= 50.0 / (select * from XXXX) %s 
  LIMIT 50"""
  query = query % (full_tablename, where, full_tablename, where)
  params = params + params

  manager = DataHubManager(user=username)
  res = manager.execute_sql(query, params=params)
  rows = res['tuples']
  cols = [field['name'] for field in res['fields']]

  data = [dict(zip(cols, vals)) for vals in rows]
  ret['data'] = data
  ret['schema'] = get_schema(dbname, table, username)

  print "%d points returned" % len(ret.get('data', []))
  return ret



@returns_json
def api_query(request):
  ret = { }
  jsonstr = request.GET.get('json', None)
  if not jsonstr:
    print "query: no json string.  giving up"
    return ret

  args = json.loads(jsonstr)
  username = args.get('username')
  dbname = args.get('db')
  table = args.get('table')
  args['table'] = "%s.%s" % (dbname, table)

  o, params = create_sql_obj(None, args)
  o.limit = 10000;
  query = str(o)
  print query
  print params

  if not dbname or not table or not query:
    print "query: no db/table/query.  giving up"
    return ret

  manager = DataHubManager(user=username)
  res = manager.execute_sql(query, params)
  rows = res['tuples']
  cols = pick(res['fields'], 'name')

  data = [dict(zip(cols, vals)) for vals in rows]
  ret['data'] = data
  ret['schema'] = get_schema(dbname, table, username)

  print "%d points returned" % len(ret.get('data', []))
  return ret



@returns_json
def column_distribution(request):
  username = request.GET.get('username')
  dbname = request.GET.get('db', 'intel')
  tablename = request.GET.get('table', 'readings')
  where = request.GET.get('where', '')
  col = request.GET.get('col')
  try:
    nbuckets = int(request.GET.get('nbuckets', 100))
  except Exception as e:
    print e
    nbuckets = 100

  full_tablename = "%s.%s" % (dbname, tablename)

  summary = Summary(dbname, full_tablename, username, nbuckets=nbuckets, where=where)
  try:
    typ = summary.get_type(col)
    stats = summary.get_col_stats(col, typ)
  except Exception as e:
    traceback.print_exc()
  finally:
    summary.close()

  data = {
    'col': col,
    'type': typ,
    'stats': stats
  }
  context = { "data": data }
  return context



@returns_json
def column_distributions(request):
  username = request.GET.get('username')
  dbname = request.GET.get('db', 'intel')
  tablename = request.GET.get('table', 'readings')
  where = request.GET.get('where', '')
  try:
    nbuckets = int(request.GET.get('nbuckets', 100))
  except Exception as e:
    print e
    nbuckets = 100

  full_tablename = "%s.%s" % (dbname, tablename)
  summary = Summary(dbname, full_tablename, username, nbuckets=nbuckets, where=where)
  print 'where: %s' % where
  try:
    stats = summary()
  except Exception as e:
    traceback.print_exc()
  finally:
    summary.close()


  data = []
  for col, typ, col_stats in stats:
    data.append({
      'col': col, 
      'type': typ, 
      'stats': col_stats
    })

  context = { "data": data }
  return context



@returns_json
def scorpion(request):
  if not has_scorpion():
    print >>sys.stderr, "Could not load scorpionutil.  Maybe scorpion has not been installed?"
    return {'status': "error: could not load scorpion"}

  try:
    data =  json.loads(str(request.GET.get('json')))
    username = request.GET.get('username')
    fake = request.GET.get('fake', False)
    requestid = request.GET.get('requestid')
    if not fake or fake == 'false':

      import core.db.backend.pg as pg
      qjson = data.get('query', {})
      repo = qjson['db']
      qjson['db'] = username
      qjson['table'] = "%s.%s" % (repo, qjson['table'])
      tablename = qjson['table']
      host = pg.host
      port = pg.port
      dburl = "postgresql://%s@%s:%s/%s" % (username,host, port, username)
      engine = create_engine(dburl)
      db = engine.connect()
      import scorpionutil

      try:
        results = scorpionutil.scorpion_run(db, data, requestid)
        return results
      except:
        traceback.print_exc()
        return {}
      finally:
        try:
          db.close()
        except:
          pass
        try:
          engine.dispose()
        except:
          pass


  except:
    traceback.print_exc()
    return {}

  ret = {}
  results = [
    {
      'score': 0.2,
      'c_range': [0, 1],
      'count': 100,
      'clauses': [
        {'col': 'sensor', 'type': 'str', 'vals': map(str, [18])}
      ],
      'alt_rules': [
        [ {'col': 'humidity', 'type': 'num', 'vals': [0, 1.4]}]
      ]
    },
    {
      'score': 0.2,
      'c_range': [0, 1],
      'count': 100,
      'clauses': [
        {'col': 'voltage', 'type': 'num', 'vals': [0, 2.15]},
        {'col': 'sensor', 'type': 'str', 'vals': ['18']}
      ],
      'alt_rules': [
        [ {'col': 'humidity', 'type': 'num', 'vals': [0, 1.4]},
          {'col': 'humidity', 'type': 'num', 'vals': [0, 1.4]} ],
        [ {'col': 'humidity', 'type': 'num', 'vals': [0, 1.4]},
          {'col': 'humidity', 'type': 'num', 'vals': [0, 1.4]} ]
      ]
    }
  ]

  top_k = [
    {
      'c': 0,
      'score': 0.2,
      'c_range': [0, 0],
      'count': 100,
      'clauses': [
        {'col': 'sensor', 'type': 'str', 'vals': map(str, [18])}
      ]
    },
    {
      'c': 0,
      'score': 0.2,
      'c_range': [0, 0],
      'count': 100,
      'clauses': [
        {'col': 'voltage', 'type': 'num', 'vals': [0, 2.15]},
        {'col': 'sensor', 'type': 'str', 'vals': ['18']}
      ]
    },
    {
      'c': 0.5,
      'score': 0.2,
      'c_range': [0.5, .5],
      'count': 100,
      'clauses': [
        {'col': 'sensor', 'type': 'str', 'vals': map(str, [18, 15])}
      ]
    },
    {
      'c': 0.5,
      'score': 0.2,
      'c_range': [0.5, .5],
      'count': 100,
      'clauses': [
        {'col': 'voltage', 'type': 'num', 'vals': [-5, 2.5]},
        {'col': 'sensor', 'type': 'str', 'vals': ['18', '15']}
      ]
    },
    {
      'c': 1.0,
      'score': 0.2,
      'c_range': [1.0, 1.0],
      'count': 100,
      'clauses': [
        {'col': 'sensor', 'type': 'str', 'vals': map(str, [18, 30, 35])}
      ]
    },
    {
      'c': 1.0,
      'score': 0.2,
      'c_range': [1.0, 1.0],
      'count': 100,
      'clauses': [
        {'col': 'humidity', 'type': 'num', 'vals': [-100, 40]},
        {'col': 'sensor', 'type': 'str', 'vals': ['18', '19']}
      ]
    }

  ]

  from scorpion.util import Status
  status = Status(requestid)
  status.update_rules('label', results)
  status.close()

  time.sleep(1)

  ret['results'] = results
  ret['top_k_results'] = top_k
  return ret


