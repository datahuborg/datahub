from backend.sqlversioning import SQLVersioning
import logging


log = logging.getLogger('dh')
logging.basicConfig()
log.setLevel(logging.INFO)


class SystemVersioning:
  def __init__(self):
    self.backend = SQLVersioning()
  
  #given a version and display name, find table real name (tail only, not chain of tables)
  def find_active_table(self, version, display_table_name):
    if isinstance(version, basestring):
      v_id = self.backend.get_v_id(repo,v_name)
    else:
      v_id = version
    return self.backend.find_active_table(v_id ,display_table_name)
  
  #get a select * from table that unions and filters based on table ancestors
  def build_table_query(self, table_tail, pkey='id'):
    return self.backend.build_table_query(table_tail, pkey)
  
  def gen_string(self,base='', n=6):
    return self.backend.gen_string(base,n)
  
  #TODO
  def get_read_rs(self,sql, table_names, version):
    log.info("get_rs : %s" % table_names)
    if isinstance(table_names,str):
      table_names = [ table_names]
    log.info("Dirty hack alert. need to replace with parser")
    for t in table_names:
      active_table = self.backend.find_active_table(version, t)
      log.debug("%s:%s" % (t, active_table))      
      replace = self.backend.build_table_query(active_table)
      log.debug(replace)
      sql = sql.replace(t,replace)
    
    log.info(sql)           
    return self.backend.get_rs(sql)

  #TODO
  def get_update_rs(self,sql, table_names, version):
    log.info("get_rs : %s" % table_names)
    if isinstance(table_names,str):
      table_names = [ table_names]
    #TODO check if COW
    raise Exception("COW")
    log.info("Dirty hack alert. need to replace with parser")
    for t in table_names:
      active_table = self.backend.find_active_table(version, t)
      log.debug("%s:%s" % (t, active_table))      
      sql = sql.replace(t,active_table)
    
    log.info(sql)           
    return self.backend.get_rs(sql)
  
    
  def freeze_table(self, table_real_name):    
    return self.backend.freeze_table(table_real_name)  
  #Freeze (COW flag) tables for a version  
  def freeze_tables(self, v_id):    
    return self.backend.freeze_tables(v_id)


  #add a new table to a version
  def add_table(self, table_name, create_sql, version, repo, user):
    if isinstance(version, basestring):
      v_id = self.backend.get_v_id(repo,v_name)
    else:
      v_id = version
    self.create_table( user, repo, table_name, create_sql, v_id)
  
  #add a new table to a version
  def create_table(self, user, repo, table_display_name, create_sql, v_id, rn = None):
    return self.backend.create_table(user, repo, table_display_name, create_sql, v_id, rn)

  def clone_version(self, old_v_id, new_v_id):
    tables = self.backend.get_list_tables(old_v_id)
    log.info("Tables in v_id:%s to clone:%s"% (old_v_id, tables))
    for table in tables:
      clone_table(table, new_v_id)

  #Call when a COW frozen table needs to be cloned for an insert. returns new table real name
  def clone_table(self,table_real_name, new_v_id, new_name=None):
    #Assert froze
    self.freeze_table(table_real_name)
    #Create table 
    #return table_real_name
    return self.backend.clone_table(table_real_name, new_v_id, new_name)
  
  #TODO
  def get_query_trace(self, v_id1, v_id2):
    return self.backend.get_query_trace(v_id1, v_id2)
  
  #TODO
  def update_user_head(self, user, repo, v_id=None, v_name=None):
    log.info("update user head TODO...")
    return self.backend.check_v_id(v_id)
    #return self.backend.update_user_head(user, repo, v_id, v_name)
  
  #create a new version, or fork an existing version id
  def create_version(self, user, repo, v_name, parent_v_id=None):
    log.debug("create version")
    if parent_v_id:
      self.freeze_tables(parent_v_id)
    return self.backend.create_version(user, repo, v_name, parent_v_id)
  
  def get_versions(self, user, repo):
    return self.backend.get_versions(user, repo)
  
  #TODO
  def commit(self, query_list, v_id):
    #update query log
    #insert into active table of v
    return self.backend.commit(query_list, v_id)
    
  
    
    