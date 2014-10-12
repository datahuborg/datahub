import hashlib

from core.db import connection
from core.db.manager import DataHubManager

from datahub import DataHub
from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Handler
'''

def construct_result_set(res):
  tuples = [Tuple(
      cells=[bytes(val) for val in t]) for t in res['tuples']]

  field_names = [bytes(field['name']) for field in res['fields']]
  field_types = [bytes(field['type']) for field in res['fields']]
  
  return ResultSet(status=res['status'],
                   num_tuples=res['row_count'],
                   num_more_tuples=0,
                   tuples=tuples,
                   field_names=field_names,
                   field_types=field_types)


class DataHubHandler:
  def __init__(self):
    self.sessions={}
    pass

  def get_version(self):
    return VERSION

  def open_connection(self, con_params):  
    try:
      db_con = connection.Connection(
          user=con_params.user,
          password=hashlib.sha1(con_params.password).hexdigest())

      con = Connection(
          user=con_params.user,
          repo_owner=con_params.repo_owner,
          repo=con_params.repo)
      
      return con
    except Exception, e:
      raise DBException(message=str(e))
  
  def create_repo(self, con, repo_name):
    try:
      manager = DataHubManager(user=con.user, database=con.repo_owner)
      res = manager.create_repo(repo=repo_name)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def list_repos(self, con):
    try:
      manager = DataHubManager(user=con.user, database=con.repo_owner)
      res = manager.list_repos()
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def delete_repo(self, con, repo_name, force_if_non_empty):
    try:
      manager = DataHubManager(user=con.user, database=con.repo_owner)
      res = manager.delete_repo(repo=repo_name, force=force_if_non_empty)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def list_tables(self, con, repo_name):
    try:
      manager = DataHubManager(user=con.user, database=con.repo_owner)
      res = manager.list_tables(repo=repo_name)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def print_schema(self, con, table_name):
    try:
      manager = DataHubManager(user=con.user, database=con.repo_owner)
      res = manager.print_schema(table=table_name)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))

  def execute_sql(self, con, query, query_params=None):
    try:
      manager = DataHubManager(user=con.user, database=con.repo_owner)
      res = manager.execute_sql(query=query, params=query_params)
      return construct_result_set(res)
    except Exception, e:
      raise DBException(message=str(e))