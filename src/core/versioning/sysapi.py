from backend.sqlversioning import SQLVersioning

class SystemVersioning:
  def __init__(self):
    self.backend = SQLVersioning()
    
  def find_active_table(self, version, display_table_name):
    return self.backend.find_active_table(version,display_table_name)
  
  
  def build_table_query(self, table_tail):
    return self.backend.build_table_query(table_tail)
  
  def get_rs(self,sql):
    return self.backend(sql)
  

    
  def freeze_table(self, table_real_name):    
    return self.backend.freeze_table(table_real_name)  
    
  def freeze_tables(self, v_id):    
    return self.backend.freeze_tables(v_id)

  def add_table(self, table_name, create_sql, version, repo, user):
    if isinstance(version, basestring):
      v_id = self.backend.get_v_id(repo,v_name)
    else:
      v_id = version
    self.create_table( user, repo, table_name, create_sql, v_id)
  
  def create_table(self, user, repo, table_display_name, create_sql, v_id):
    return self.backend.create_table(user, repo, table_display_name, create_sql, v_id)

  def clone_table(self,table_real_name, new_v_id, new_name=None):
    #Assert froze
    self.freeze_table(table_real_name)
    #Create table 
    #return table_real_name
    return self.backend.clone_table(table_real_name, new_v_id, new_name)
    
  def get_query_trace(self, v_id1, v_id2):
    return self.backend.get_query_trace(v_id1, v_id2)
  
  def update_user_head(self, user, repo, v_id=None, v_name=None):
    return self.backend.update_user_head(user, repo, v_id, v_name)
  
  def create_version(self, user, repo, v_name, parent_v_id=None):
    if parent_v_id:
      self.freeze_tables(parent_v_id)
    return self.backend.create_version(user, repo, v_name, parent_v_id)
  
  def commit(self, query_list, v_id):
    #update query log
    #insert into active table of v
    return self.backend.commit(query_list, v_id)
    
  
    
    