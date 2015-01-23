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




class DataHubSession:
  def __init__(self, user='test', repo='test'):
    log.info("DataHubSession init")
    self.sv = SystemVersioning()
    self.user = user
    self.repo = repo
    self.current_version = None
  
  def init(self, user, repo):
    log.info("TODO check if repo exists. if so use default version") #TODO
    version_name = self.get_random_hash()
    self.sv.create_version(self.user, self.repo, version_name)

  def init_new_version_with_table(self, table, data_con=None):
    version_name = self.get_random_hash()
    v_id = self.sv.create_version(self.user, self.repo, version_name)
    log.info("created version:%s now init existing table%s" %(v_id,table))
    res= self.sv.init_existing_table(self.user, self.repo, table, v_id, data_con=data_con)
    log.info("imported existing table")
    self.sv.update_user_head(self.user, self.repo, v_id=v_id)
    return res
    

  def get_random_hash(self):
    return self.sv.gen_string()

  def branch(self, arg=''):
    log.info("Getting versions for %s %s " % (self.user, self.repo))
    return self.sv.get_versions(self.user, self.repo)

  def clone(self, v_id):
    new_version = self.get_random_hash()
    self.sv.create_version(self.user, self.repo, new_version, v_id)
    #From old clone table self.sv.clone_table(table_name, table_name + '_' + version_id)

  def checkout(self,  v_id):
    res = self.sv.update_user_head(self.user, self.repo, v_id=v_id)
    if res:
      self.current_version = v_id
    return res
  
  def stash(self, table_name):
    self.sv.stash(table_name)

  def commit(self, table_name):
    version_id = self.get_random_hash()
    self.sv.create_version(self.user, self.repo, version_id)
    # TODO

  def diff(self, table_name, v_id=None):
    self.sv.diff(table_name, v_id)

  #TODO
  def sql(self, query):
    if not self.current_version:
      raise Exception('Must checkout a version first')
    
    t = sqlparse.parse(query)
    table_names = extract_tables.extract_tables(query)
    
    while 'values' in table_names:
      table_names.remove('values')
    while 'VALUES' in table_names:
      table_names.remove('VALUES')    
    log.info("table names: %s \t\tHACK remove values strip" % table_names) #TODO remove the above hack
    
    #TODO " in sql causes some issues with psql
    
    op_type = t[0].get_type()
    if op_type.upper() in ['CREATE']:
      log.info("TODO how to parse PKey?")#TODO
      table_rn = self.sv.create_table(self.user, self.repo, table_names[0], query, self.current_version)      
      return "Created table %s with real name %s" % (table_names[0], table_rn)
    elif op_type.upper() in ['INSERT', 'UPDATE']:
      log.debug("insert/update")
      return self.sv.get_update_rs(query, table_names, self.current_version)
    elif op_type.upper() in ['SELECT']:
      log.debug("select")
      return self.sv.get_read_rs(query,table_names, self.current_version)
      
      
  
    
    