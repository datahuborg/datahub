from sysapi import SystemVersioning
import random
import sqlparse
import logging
import extract_tables
'''
@author: anant bhardwaj
@date: Dec 8, 2014

versioning session manager
'''
log = logging.getLogger('dh')
logging.basicConfig()
log.setLevel(logging.INFO)

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

  def branch(self, arg):
    return self.sv.get_versions(self.user, self.repo)

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
    table_names = extract_tables.extract_tables(query)
    log.info(table_names)
    #table_name = t[0].get_name()
    op_type = t[0].get_type()
    if op_type.ipper() in ['CREATE']:
      pass
    elif op_type.upper() in ['INSERT', 'UPDATE']:
      self.sv.rs(query)
  
    
    