from sysapi import SystemVersioning
import random
import sqlparse

'''
@author: anant bhardwaj
@date: Dec 8, 2014

versioning session manager
'''

def get_random_hash():
  return str(hex(random.getrandbits(128)))

class DataHubSession:
  def __init__(self):
    self.sv = SystemVersioning()
    self.user = 'test'
    self.repo = 'test'
  
  def init(self, table_name):
    version_id = get_random_hash()
    self.sv.create_version(self.user, self.repo, version_id)
    self.sv.rename_table(self.user, self.repo, table_name, version_id)

  def clone(self, table_name):
    version_id = get_random_hash()
    self.sv.clone_table(table_name, table_name + '_' + version_id)

  def checkout(self, table_name, v_id):
    self.sv.set_version(table_name, v_id)
  
  def stash(self, table_name):
    self.sv.stash(table_name)

  def commit(self, table_name):
    version_id = get_random_hash()
    self.sv.create_version(self.user, self.repo, version_id)
    # TODO

  def diff(self, table_name, v_id=None):
    self.sv.diff(table_name, v_id)

  #TODO
  def sql(self, query):
    t = sqlparse.parse(query)
    table_name = t[0].get_name()
    op_type = t[0].get_type
      
    if op_type in ['INSERT', 'UPDATE']:
      self.sv.rs(query)
  
    
    