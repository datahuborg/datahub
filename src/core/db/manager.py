import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config import settings
from core.db.connection import DataHubConnection
from schema.models import *


'''
Datahub DB Manager

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

class DataHubManager:
  def __init__(self, user, repo_base=None):
    self.user = User.objects.get(username=user)
    self.user_con = DataHubConnection(
        user=self.user.username,
        repo_base=repo_base,
        password=self.user.password)
  
  ''' Basic Operations. '''

  def reset_connection(self, repo_base):
    self.user_con.reset_connection(repo_base=repo_base)

  def close_connection(self):    
    self.user_con.close()
  
  def create_repo(self, repo):  
    return self.user_con.create_repo(repo=repo)

  def list_repos(self):
    return self.user_con.list_repos()

  def delete_repo(self, repo, force=False):
    return self.user_con.delete_repo(repo=repo, force=force)

  def list_tables(self, repo):
    return self.user_con.list_tables(repo=repo)

  def get_schema(self, table):
    return self.user_con.get_schema(table=table)

  def execute_sql(self, query, params=None):
    return self.user_con.execute_sql(query=query, params=params)


  '''
  The following methods run in superuser mode only
  '''
  
  ''' User/Role Management '''
  
  @staticmethod
  def create_user(username, password):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.create_user(username=username, password=password)

  @staticmethod
  def change_password(username, password):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.change_password(username=username, password=password)

  ''' Import/Export Files '''
  
  @staticmethod
  def import_file(repo_base, table_name, file_path):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.import_file(
        table_name=table_name, file_path=file_path)

  @staticmethod
  def export_file(repo_base, table_name, file_path):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.export_file(
        table_name=table_name, file_path=file_path)

  ''' Access Privilege Checks '''

  @staticmethod
  def has_connect_privilege(login, repo_base, privilege):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.has_connect_privilege(
        login=login, privilege=privilege)

  @staticmethod
  def has_repo_privilege(login, repo_base, repo, privilege):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.has_repo_privilege(
        login=login, repo=repo, privilege=privilege)

  @staticmethod
  def has_table_privilege(login, repo_base, table, privilege):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.has_table_privilege(
        login=login, table=table, privilege=privilege)

  @staticmethod
  def has_column_privilege(login, repo_base, table, column, privilege):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.has_column_privilege(login=login,
        table=table, column=column, privilege=privilege)

  @staticmethod
  def list_collaborators(repo_base, repo):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.list_collaborators(repo_base=repo_base, repo=repo)