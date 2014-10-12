import os

from config import settings
from core.db.connection import *
from schema.models import *


'''
Datahub DB Manager

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

# A superuser connection for superuser tasks
superuser_con = Connection(
    user=settings.DATABASES['default']['USER'],
    password=settings.DATABASES['default']['USER'])

class DataHubManager:
  def __init__(self, user, database=None):
    self.user = User.objects.get(username=user)
    self.user_con = Connection(
        user=self.user.username,
        database=database,
        password=self.user.password)
  
  def reset_connection(self, database):
    self.user_con.reset_connection(database=database)

  def close_connection(self):    
    self.user_con.close()
  
  def create_repo(self, repo):  
    return user_con.create_repo(repo=repo)

  def list_repos(self):
    return self.user_con.list_repos()

  def delete_repo(self, repo, force=False):
    return self.user_con.delete_repo(repo=repo, force=force)

  def list_tables(self, repo):
    return self.user_con.list_tables(repo=repo)

  def print_schema(self, table):
    return self.user_con.print_schema(table=table)

  def execute_sql(self, query, params=None):
    return self.user_con.execute_sql(query=query, params=params)


  '''
  The following methods run in superuser mode
  '''
  
  @staticmethod
  def import_file(repo_owner, path, table_name):
    superuser_con.reset_connection(database=repo_owner)
    return superuser_con.import_file(
        username=username, path=path, table_name=table_name)

  @staticmethod
  def export_file(repo_owner, path, table_name):
    superuser_con.reset_connection(database=repo_owner)
    return superuser_con.export_file(
        username=username, path=path, table_name=table_name)

  @staticmethod
  def create_user(username, password):
    return superuser_con.create_user(username=username, password=password)

  @staticmethod
  def change_password(username, password):
    return superuser_con.change_password(username=username, password=password)

  @staticmethod
  def list_shared_repos(username):
    superuser_con.reset_connection(database=username)
    return superuser_con.list_shared_repos(username=username)

  @staticmethod
  def has_user_access_privilege(login, repo_owner, privilege):
    return superuser_con.has_user_access_privilege(
        login=login, username=repo_owner, privilege=privilege)

  @staticmethod
  def has_repo_privilege(login, repo_owner, repo, privilege):
    superuser_con.reset_connection(database=repo_owner)
    return superuser_con.has_repo_privilege(
        login=login, username=username, repo=repo, privilege=privilege)

  @staticmethod
  def has_table_privilege(login, repo_owner, table, privilege):
    superuser_con.reset_connection(database=repo_owner)
    return superuser_con.has_table_privilege(
        login=login, username=username, table=table, privilege=privilege)

  @staticmethod
  def has_column_privilege(login, repo_owner, repo, column, privilege):
    superuser_con.reset_connection(database=repo_owner)
    return superuser_con.has_column_privilege(login=login,
        username=username, table=table, column=column, privilege=privilege)