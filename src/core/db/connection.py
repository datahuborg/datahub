import psycopg2
import re

from backend.pg import PGBackend
from config import settings

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub DB wrapper for backends (only postgres implemented)
'''
superuser_backend = PGBackend(
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['USER'])

class Connection:
  def __init__(self, user, password):
    self.user_backend = PGBackend(user, password)
  
  def create_repo(self, repo):
    return self.user_backend.create_repo(repo=repo)

  def list_repos(self):
    return self.user_backend.list_repos()

  def delete_repo(self, repo, force=False):
    return self.user_backend.delete_repo(repo=repo, force=force)

  def list_tables(self, repo):
    return self.user_backend.list_tables(repo=repo)

  def print_schema(self, table):
    return self.user_backend.print_schema(table=table)

  def execute_sql(self, query, params=None):
    return self.user_backend.execute_sql(query, params) 

  def close(self):    
    self.user_backend.close()

  '''
  The following methods run in superuser mode
  '''
  @staticmethod
  def create_user(username, password):
    return superuser_backend.create_user(username, password)

  @staticmethod
  def import_file(username, path, table_name):
    superuser_backend.reset_connection(database=username)
    return superuser_backend.import_file(path=path, table_name=table_name)

  @staticmethod
  def export_file(username, path, table_name):
    superuser_backend.reset_connection(database=username)
    return superuser_backend.export_file(path=path, table_name=table_name)

  @staticmethod
  def change_password(username, password):
    return superuser_backend.change_password(username, password)

  @staticmethod
  def list_shared_repos(username):
    superuser_backend.reset_connection(database=username)
    return superuser_backend.list_shared_repos(username)

  @staticmethod
  def has_user_access_privilege(login, username, privilege):
    return superuser_backend.has_user_access_privilege(
        login=login, username=username, privilege=privilege)

  @staticmethod
  def has_repo_privilege(login, username, repo, privilege):
    superuser_backend.reset_connection(database=username)
    return superuser_backend.has_repo_privilege(
        login=login, repo=repo, privilege=privilege)

  @staticmethod
  def has_table_privilege(login, username, table, privilege):
    superuser_backend.reset_connection(database=username)
    return superuser_backend.has_table_privilege(
      login=login, table=table, privilege=privilege)

  @staticmethod
  def has_column_privilege(login, username, table, column, privilege):
    superuser_backend.reset_connection(database=username)
    return superuser_backend.has_column_privilege(
        login=login, table=table, column=column, privilege=privilege)