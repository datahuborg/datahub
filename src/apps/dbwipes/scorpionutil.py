import os
import re
import time
import json
import md5
import pdb
import psycopg2
import traceback
import numpy.random as nprand

from collections import *
from datetime import datetime

from browser.auth import *
from django.db import connection

from scorpionsql.aggerror import AggErr
from scorpion.arch import SharedObj, extract_agg_vals
from scorpion.parallel import parallel_debug
from scorpion.util import Status

from util import *


def scorpion_run(db, requestdata, requestid):
  """
  badsel:  { alias: { x:, y:, xalias:, yalias:, } }
  goodsel: { alias: { x:, y:, xalias:, yalias:, } }
  """
  from db import db_type
  context = {}

  try:
    qjson = requestdata.get('query', {})
    dbname = qjson['db']
    tablename = qjson['table']
    parsed, params = create_sql_obj(db, qjson)
    print "parsed SQL"
    print parsed
  except Exception as e:
    traceback.print_exc()
    context["error"] = str(e)
    return context



  try:    
    badsel = requestdata.get('badselection', {})
    goodsel = requestdata.get('goodselection', {})
    errtypes = requestdata.get('errtypes', {})
    erreqs = requestdata.get('erreqs', {})
    ignore_attrs = requestdata.get('ignore_cols', [])
    x = qjson['x']
    ys = qjson['ys']

    obj = SharedObj(db, dbname=dbname, parsed=parsed, params=params)
    obj.dbname = dbname
    obj.C = 0.2
    obj.ignore_attrs = map(str, ignore_attrs )

    # fix aliases in select
    for nonagg in obj.parsed.select.nonaggs:
      nonagg.alias = x['alias']
    for agg in obj.parsed.select.aggs:
      y = [y for y in ys if y['expr'] == agg.expr][0]
      agg.alias = y['alias']


    xtype = db_type(db, tablename, x['col'])

    errors = []
    for agg in obj.parsed.select.aggregates:
      alias = agg.shortname
      if alias not in badsel:
        continue

      badpts = badsel.get(alias, [])
      badkeys = map(lambda pt: pt['x'], badpts)
      badkeys = extract_agg_vals(badkeys, xtype)
      goodpts = goodsel.get(alias, [])
      goodkeys = map(lambda pt: pt['x'], goodpts)
      goodkeys = extract_agg_vals(goodkeys, xtype)
      errtype = errtypes[alias]
      print "errtype", errtype
      erreq = []
      if errtype == 1:
        erreq = erreqs[alias]
        print "erreq", erreq


      # XXX: for better end-to-end performance
      #      sample the badkeys and goodkeys so there are ~20
      if len(badkeys) > 20:
        idxs = range(len(badkeys))
        newidxs = nprand.choice(idxs, 20, False)
        badkeys = map(badkeys.__getitem__, newidxs)
        if erreq:
          erreq = map(erreq.__getitem__, newidxs)
      if len(goodkeys) > 20:
        idxs = range(len(goodkeys))
        newidxs = nprand.choice(idxs, 20, False)
        goodkeys = map(goodkeys.__getitem__, newidxs)


      err = AggErr(agg, badkeys, 20, errtype, {'erreq': erreq})
      obj.goodkeys[alias] = goodkeys
      errors.append(err)

    obj.errors = errors

    obj.status = Status(requestid)
    print "status requid = ", requestid

    start = time.time()
    print obj.rules_schema
    parallel_debug(
      obj,
      parallel=True,
      nstds=0,
      errperc=0.001,
      epsilon=0.008,
      msethreshold=0.15,
      tau=[0.001, 0.05],
      c=obj.c,
      complexity_multiplier=4.5,
      l=0.7,
      c_range=[0.1, 1.],
      max_wait=20,
      use_cache=False,
      granularity=20,
      ignore_attrs=obj.ignore_attrs,
      DEBUG=False
    )
    cost = time.time() - start
    print "end to end took %.4f" % cost


    obj.update_status('serializing results')
    context['results'] = encode_best_rules(obj)
    context['top_k_results'] = encode_top_k(obj)

    obj.update_status('done!')

  except Exception as e:
    traceback.print_exc()
    context['error'] = str(e)
  finally:
    try:
      obj.status.close()
    except:
      pass


  return context

def encode_best_rules(obj):
  """
  Given the resulting rule clusters, package them into renderable
  JSON objects
  """
  from scorpion.learners.cn2sd.rule import rule_to_json
  results = []
  for yalias, rules in obj.rules.items():
    for rule in rules:
      result = rule_to_json(rule, yalias=yalias)
      results.append(result)
  return results

def encode_top_k(obj):
  """
  extract the top_k per c_value and encode as a dictionary:
  {
    c_val: [json_rules in descending influence order]
  }
  """
  from scorpion.learners.cn2sd.rule import rule_to_json
  results = [] #defaultdict(lambda: defaultdict(list))
  for yalias, top_k_rules in obj.top_k_rules.items():
    for c_val, rules in top_k_rules.iteritems():
      for rule in rules:
        rule.c_range = [c_val, c_val]
        result = rule_to_json(rule, yalias=yalias)
        result['c'] = round(c_val, 3)
        results.append(result)
        #results[yalias][c_val].append(result)
  return results


