import psycopg2
import re

from backend.pg import PGBackend

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub DB wrapper for backends (only postgres implemented)
Any new backend must implement the Connection interface
'''

class Connection:
  def __init__(self, user, password, database=None):
    self.backend = PGBackend(user, password, database=database)
  
  def reset_connection(self, database):
    self.backend.reset_connection(database=database)

  def close_connection(self):    
    self.backend.close_connection()

  def create_repo(self, repo):
    return self.backend.create_repo(repo=repo)

  def list_repos(self):
    return self.backend.list_repos()

  def delete_repo(self, repo, force=False):
    return self.backend.delete_repo(repo=repo, force=force)

  def share_repo(self, repo, username, auto_in_future=True):
    return self.backend.share_repo(
        repo=repo, username=username, auto_in_future=auto_in_future)

  def list_tables(self, repo):
    return self.backend.list_tables(repo=repo)

  def print_schema(self, table):
    return self.backend.print_schema(table=table)

  def execute_sql(self, query, params=None):
    return self.backend.execute_sql(query, params) 


  '''
  The following methods may require superuser
  '''

  def create_user(username, password):
    return self.backend.create_user(username, password)

  def import_file(username, path, table_name):
    return self.backend.import_file(path=path, table_name=table_name)

  def export_file(username, path, table_name):
    return self.backend.export_file(path=path, table_name=table_name)

  def change_password(username, password):
    return self.backend.change_password(username, password)

  def list_shared_repos(username):
    return self.backend.list_shared_repos(username)

  def has_user_access_privilege(login, username, privilege):
    return self.backend.has_user_access_privilege(
        login=login, username=username, privilege=privilege)

  def has_repo_privilege(login, username, repo, privilege):
    return self.backend.has_repo_privilege(
        login=login, repo=repo, privilege=privilege)

  def has_table_privilege(login, username, table, privilege):
    return self.backend.has_table_privilege(
      login=login, table=table, privilege=privilege)

  def has_column_privilege(login, username, table, column, privilege):
    return self.backend.has_column_privilege(
        login=login, table=table, column=column, privilege=privilege)