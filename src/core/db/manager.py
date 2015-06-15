import hashlib
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config import settings
from core.db.connection import DataHubConnection
from inventory.models import *


'''
Datahub DB Manager

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

class DataHubManager:
  def __init__(self, user, repo_base=None, is_app=False):
    username = None
    password = None
    
    if is_app:
      app = App.objects.get(app_id=user)
      username = app.app_id
      password = hashlib.sha1(app.app_token).hexdigest()
    else:
      user = User.objects.get(username=user)
      username = user.username
      password = user.password
    
    self.user_con = DataHubConnection(
        user=username,
        repo_base=repo_base,
        password=password)
  
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

  def list_views(self, repo):
    return self.user_con.list_views(repo=repo)

  def get_schema(self, table):
    return self.user_con.get_schema(table=table)

  def execute_sql(self, query, params=None):
    return self.user_con.execute_sql(query=query, params=params)

  def add_collaborator(self, repo, username, privileges, auto_in_future=True):
    return self.user_con.add_collaborator(
        repo=repo,
        username=username,
        privileges=privileges,
        auto_in_future=auto_in_future)

  def delete_collaborator(self, repo, username):
    return self.user_con.delete_collaborator(repo=repo, username=username)


  '''
  The following methods run in superuser mode only
  '''
  
  ''' User/Role Management '''
  
  @staticmethod
  def create_user(username, password, create_db=True):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.create_user(
        username=username, password=password, create_db=create_db)

  @staticmethod
  def remove_user(username):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.remove_user(username=username)

  @staticmethod
  def change_password(username, password):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'])
    return superuser_con.change_password(username=username, password=password)

  ''' Import/Export Files '''
  
  @staticmethod
  def import_file(repo_base, table_name, file_path, file_format='CSV',
      delimiter=',', header=True, encoding='ISO-8859-1', quote_character='"'):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.import_file(
        table_name=table_name,
        file_path=file_path,
        file_format=file_format,
        delimiter=delimiter,
        header=header,
        encoding=encoding,
        quote_character=quote_character)

  @staticmethod
  def export_table(repo_base, table_name, file_path, file_format='CSV',
      delimiter=',', header=True):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.export_table(
        table_name=table_name,
        file_path=file_path,
        file_format=file_format,
        delimiter=delimiter,
        header=header)

  @staticmethod
  def export_query(repo_base, query, file_path, file_format='CSV',
      delimiter=',', header=True):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.export_query(
        query=query,
        file_path=file_path,
        file_format=file_format,
        delimiter=delimiter,
        header=header)

  ''' Access Privilege Checks '''

  @staticmethod
  def has_base_privilege(login, repo_base, privilege):
    superuser_con = DataHubConnection(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.has_base_privilege(
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
        password=settings.DATABASES['default']['USER'],
        repo_base=repo_base)
    return superuser_con.list_collaborators(repo_base=repo_base, repo=repo)