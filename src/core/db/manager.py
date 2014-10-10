import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from core.db.connection import *
from schema.models import *


'''
Datahub DB Manager

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''
def create_repo(username, repo):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password)
  return con.create_repo(repo=repo)

def list_repos(username):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password)
  res = con.list_repos()
  return res

def delete_repo(username, repo, force):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password)
  return con.delete_repo(repo=repo, force=force)

def list_tables(username, repo):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password)
  res = con.list_tables(repo=repo)
  return res

def print_schema(username, table):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password)
  res = con.print_schema(table=table)
  return res

def execute_sql(username, query, params=None):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password)
  res = con.execute_sql(query=query, params=params)
  return res

'''
SUPERUSER operations (be careful)
'''

def create_table_from_file(path, database, table_name):
  res = Connection.create_table_from_file(
      path=path, database=database, table_name=table_name)
  return res

def create_user(username, password):
  res = Connection.create_user(username=username, password=password)
  return res

def change_password(username, password):
  res = Connection.change_password(username=username, password=password)
  return res

def list_shared_repo(username):
  res = Connection.list_shared_repo(username=username)
  return res

def has_database_privilege(username, database, privilege):
  res = Connection.has_database_privilege(
      username=username, database=database, privilege=privilege)
  return res

def has_repo_privilege(username, repo, privilege):
  res = Connection.has_repo_privilege(
      username=username, repo=repo, privilege=privilege)
  return res

def has_table_privilege(username, table, privilege):
  res = Connection.has_table_privilege(
      username=username, table=table, privilege=privilege)
  return res

def has_column_privilege(username, table, column, privilege):
  res = Connection.has_column_privilege(
      username=username, table=table, column=column, privilege=privilege)
  return res