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
    return self.user_backend.print_scheme(table=table)

  def execute_sql(self, query, params=None):
    return self.user_backend.execute_sql(query, params)

  def has_database_privilege(self, username, database, privilege):
    return self.has_database_privilege(
        username=username, database=database, privilege=privilege)

  def has_repo_privilege(self, username, repo, privilege):
    return self.has_repo_privilege(
        username=username, repo=repo, privilege=privilege)

  def has_table_privilege(self, username, table, privilege):
    return self.has_table_privilege(
        username=username, table=table, privilege=privilege)

  def has_column_privilege(self, table, column, privilege):
    return self.has_column_privilege(
        username=username, table=table, column=column, privilege=privilege)

  def close(self):    
    self.user_backend.close()

  '''
  The following methods run in superuser mode
  '''
  @staticmethod
  def create_user(username, password):
    return superuser_backend.create_user(username, password)

  @staticmethod
  def create_table_from_file(path, database, table_name):
    return superuser_backend.create_table_from_file(
        path=path, table_name=table_name)

  @staticmethod
  def change_password(username, password):
    return superuser_backend.change_password(username, password)

  @staticmethod
  def list_shared_repo(username):
    return superuser_backend.list_shared_repo(username)