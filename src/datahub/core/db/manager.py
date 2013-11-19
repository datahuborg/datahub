import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from core.db.connection import *
from schema.models import *


'''
Datahub DB Manager

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

def list_repos(username):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password,
      db_name=username)
  res = con.list_schemas()
  return res

def list_tables(username, repo):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password,
      db_name=username)
  res = con.list_tables(schema=repo)
  return res

def execute_sql(username, query, params=None):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password,
      db_name=username)
  res = con.execute_sql(query=query, params=params)
  return res

'''
SUPERUSER operations (be careful)
'''

def create_user(username, password):
  res = Connection.create_user(
      username=username, password=password)
  return res

def change_password(username, password):
  res = Connection.change_password(
      username=username, password=password)
  return res

def list_databases(username):
  res = Connection.list_databases(username=username)
  return res