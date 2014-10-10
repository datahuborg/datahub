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

def import_file(username, path, table_name):
  return Connection.import_file(
      username=username, path=path, table_name=table_name)

def export_file(username, path, table_name):
  return Connection.export_file(
      username=username, path=path, table_name=table_name)

def create_user(username, password):
  return Connection.create_user(username=username, password=password)

def change_password(username, password):
  return Connection.change_password(username=username, password=password)

def list_shared_repos(username):
  return Connection.list_shared_repos(username=username)

def has_user_access_privilege(login, username, privilege):
  return Connection.has_user_access_privilege(
      login=login, username=username, privilege=privilege)

def has_repo_privilege(login, username, repo, privilege):
  return Connection.has_repo_privilege(
      login=login, username=username, repo=repo, privilege=privilege)

def has_table_privilege(login, username, table, privilege):
  return Connection.has_table_privilege(
      login=login, username=username, table=table, privilege=privilege)

def has_column_privilege(login, username, repo, column, privilege):
  return Connection.has_column_privilege(login=login,
      username=username, table=table, column=column, privilege=privilege)