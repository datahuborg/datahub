import psycopg2
import re

from backend.pg import PGBackend

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub DB wrapper for backends (only postgres implemented)
'''

class Connection:
  def __init__(self, user, password):
    self.backend = PGBackend(user, password)
  
  def create_repo(self, repo):
    return self.backend.create_repo(repo=repo)

  def list_repos(self):
    return self.backend.list_repos()

  def delete_repo(self, repo, force=False):
    return self.backend.delete_repo(repo=repo, force=force)

  def list_tables(self, repo):
    return self.backend.list_tables(repo=repo)

  def desc_table(self, table):
    return self.backend.desc_table(table=table)

  def execute_sql(self, query, params=None):
    return self.backend.execute_sql(query, params) 

  def close(self):    
    self.backend.close()

  '''
  The following methods run in superuser mode
  '''
  @staticmethod
  def create_user(username, password):
    s_backend = PGBackend(user='postgres', password='postgres')
    s_backend.create_user(username, password)
    s_backend.execute_sql('CREATE DATABASE %s WITH OWNER=%s' %(username, username))
    return s_backend.create_user(username, password)

  @staticmethod
  def change_password(username, password):
    s_backend = PGBackend(user='postgres', password='postgres')
    return s_backend.change_password(username, password)