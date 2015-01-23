from config import settings
import psycopg2
import logging
import string
import random
import re

log = logging.getLogger('dh')



CREATE_VERSION_SQL = "insert into versions (name, repo, user_id) values (%s,%s,%s) RETURNING v_id"
CREATE_VERSION_PARENT = "insert into version_parent (child_id, parent_id) values (%s,%s)"
CREATE_VERSIONED_TABLE = "insert into versioned_table (real_name, display_name, repo) values (%s,%s,%s)"
CREATE_VERSIONS_TABLE = "insert into versions_table (real_name, v_id) values (%s,%s)"
UPDATE_VERSIONS_TABLE = "update versions_table set real_name = %s where real_name = %s and v_id = %s " 
READ_VERSIONS_TABLE = "select real_name from versions_table where v_id =%s"
FREEZE_TABLES = "update versioned_table set copy_on_write = true where real_name in (select real_name from versions_table where v_id = %s)"
FREEZE_TABLE =  "update versioned_table set copy_on_write = true where real_name = %s"
COPY_VERSIONS = "insert into versions_table (real_name, v_id) select real_name, %s from versions_table where v_id = %s" 
GET_TABLE = "select real_name, display_name, repo, copy_on_write from versioned_table where real_name = %s"
GET_TABLE_DISP_COUNT = "select count(*) from versioned_table where display_name = %s and repo=%s"
MOD_TABLE_DH_ATTRS = "alter table %s add column _dh_delbit boolean default false;"
CLONE_TABLE = "CREATE TABLE %s as select * from %s with no data"
CLONE_TABLE_WITH_DATA = "CREATE TABLE %s as select * from %s"
CREATE_TABLE_PARENT= "insert into versioned_table_parent (child_table, parent_table) values (%s,%s)"
GET_TABLE_PARENT= "select parent_table from versioned_table_parent where child_table = %s"
GET_ACTIVE_TABLE = "select vt.real_name, tbl.copy_on_write from versions_table vt, versioned_table tbl where vt.v_id = %s and tbl.display_name = %s and vt.real_name = tbl.real_name; " 
GET_V_ID = "select v_id from versions where repo = %s and name = %s"
CHECK_V_ID = 'select count(*) from versions where v_id = %s'
GET_VERSIONS = "select v_id, name from versions where repo = %s"
GET_V_TABLES = '''with recursive vtp( child_table, parent_table) as (
select v.child_table, v.parent_table from versioned_table_parent v where v.parent_table = '%s'
union all
select v2.child_table, v2.parent_table from versioned_table_parent v, versioned_table_parent v2 where                               
v.child_table = v2.parent_table
)
select * from vtp;'''
GET_VERSION_CHAIN = '''with recursive ver( version, vp) as (
select v.child_id, v.parent_id from version_parent v where v.child_id = %s
union all
select v2.child_id, v2.parent_id from version_parent v, version_parent v2 where                               
v2.child_id = v.parent_id
)
select * from ver;'''
UPDATE_USER_HEAD='update user_head set head_version = %s where user_id = %s and repo= %s'
INSERT_USER_HEAD='insert into user_head (user_id, repo, head_version) select %s, %s, %s where not exists (select 1 from user_head where user_id = %s and repo = %s)'


class SQLVersioning:
  
  def __init__(self):
    self.connection = psycopg2.connect(
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
        database=settings.DATABASES['default']['NAME'])

  #Create a new version. may not have a parent
  def create_version(self, user, repo, v_name, parent_v_id=None):
    log.info("SQLV.create version user:%s repo:%s v_name:%s parent:%s" % (user, repo, v_name, parent_v_id))
    cur = self.connection.cursor()
    id = None
    try:
      cur.execute(CREATE_VERSION_SQL,(v_name,repo,user))
      r = True
      id = cur.fetchone()[0]
      log.info("Id %s" % id)
    except Exception, e:
      r = False
      log.error(e)
    if r and parent_v_id:
      try:
        if isinstance(parent_v_id, int):
          cur.execute(CREATE_VERSION_PARENT,(id, parent_v_id))  
          cur.execute(COPY_VERSIONS, (id,parent_v_id))  
          cur.execute(FREEZE_TABLES,(parent_v_id,))
        else:
          raise Exception("not supported parent type %s %s" % (parent_v_id, type(parent_v_id)))
      except Exception, e:
        r = False
        log.error(e)
        self.connection.rollback()      
    if r:
      self.connection.commit()
    cur.close()
    return id
  
  #Find the version id for a named version
  def get_v_id(self,repo,v_name):
    cur = self.connection.cursor()
    v = None
    try:
      cur.execute(GET_V_ID,(repo, v_name))
      v = cur.fetchone()[0]
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()
    return v


  #check that v_id exists
  def check_v_id(self,v_id):
    log.info("checking that v_id exists %s"% v_id)
    cur = self.connection.cursor()
    v = None
    try:
      cur.execute(CHECK_V_ID,(v_id,))
      v = cur.fetchone()[0]
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()
    return v==1
    


  
  #Find the active table to insert into given a version and table name
  def find_active_table(self, v_id, display_table_name, need_to_write=False):
    cur = self.connection.cursor()
    rn = None
    try:
      cur.execute(GET_ACTIVE_TABLE,(v_id,display_table_name))
      rn, cow = cur.fetchone()
      if need_to_write and cow:
        rn = self.clone_table(rn, v_id)
        log.info("Updated active table due to COW")
        
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()
    return rn
    
  
  def get_list_tables(self, v_id):     
    cur = self.connection.cursor()
    rn = None
    try:
      cur.execute(READ_VERSIONS_TABLE,(v_id,))
      rn = [item[0] for item in cur.fetchall()]
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()    
    return rn
  
  def get_versions(self, user, repo):
    log.info("SV : get versions %s %s" %(user,repo))
    cur = self.connection.cursor()
    rn = None
    try:
      cur.execute(GET_VERSIONS,(repo,))
      rn = [(item[0], item[1]) for item in cur.fetchall()]
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()
    return rn
    
                      
  def gen_string(self,base='', n=6):
    return "%s_%s" % (base,''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n)))
  
  #**********************
  #*** Table chain queries
  #************************
  
  def get_read_query(self,table_chain, pk):
    multi_base = 'select * from %s'
    base = '%s'
    limiter = 'where %s.%s not in (%s)' % ( '%s',pk,'%s')
    queries = []
    if len(table_chain) == 1 :
      return base % table_chain[0]
    else:
      for j,table in enumerate(table_chain):
        if j == 0:
          query = base % table        
        else:
          query = multi_base % table
        if j > 0:
          query = "%s %s" % (query,limiter)
          excludes = self.getIds(table_chain[:j], pk)
          query = query % (table,excludes)
        queries.append(query)
    return ' union '.join(queries)

  def getIds(self,tables, pk):
    select_sql = 'select %s from %s' % (pk, '%s')
    if type(tables) == list:
      return ' union '.join(select_sql % t for t in tables)
    else:
      return select_sql % tables

  
  
  def get_table_chain(self, table_tail):
    cur = self.connection.cursor()
    try:
      cur.execute(GET_TABLE_PARENT,(table_tail,))
      #TODO if has more than one parent
      res = [table_tail]
      r = cur.fetchone()
      while r:
        p = r[0]
        res.append(p)
        cur.execute(GET_TABLE_PARENT,(p,))
        r = cur.fetchone()
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()
    return res

  #TODO this assumes id exists. we need a flexible way to check for PK and if none, just union
  def build_table_query(self, table_tail, pk = 'id'):
    table_chain = self.get_table_chain(table_tail)
    query = self.get_read_query(table_chain, pk)
    return query
  
  def get_rs(self,sql):
    cur = self.connection.cursor()
    rs = None
    try:
      cur.execute(sql)
      self.connection.commit()
      rs = [row for row in cur.fetchall()]
        
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()
    return rs
    
  #Freeze all the tables associated with a version
  def freeze_tables(self, v_id):
    cur = self.connection.cursor()
    try:
      cur.execute(FREEZE_TABLES,(v_id,))
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()

  def freeze_table(self,table_real_name):
    cur = self.connection.cursor()
    try:
      cur.execute(FREEZE_TABLE,(table_real_name,))
      self.connection.commit()
    except Exception, e:
      log.error(e)
      self.connection.rollback()      
    cur.close()

  #placeholder for proper SQL parsing
  def replace_table_name(self, old_table, new_table, sql):
    return re.sub(old_table, new_table, sql)

  #Any validation of DH create statements
  def validate_extend_create_sql(self, sql):
    #Not needed now
    log.error("TODO")
    return sql
  
  def init_existing_table(self, user, repo, table_display_name, v_id, provided_rn = None, data_con=None):
    log.info("init existing table display:%s v_id:%s " % (table_display_name,v_id ))
    rn = None
    cur = self.connection.cursor()
    try:
      #Ensure that no other display name exists in the repo
      cur.execute(GET_TABLE_DISP_COUNT,(table_display_name,repo))
      cnt = cur.fetchone()[0]
      if cnt != 0:
        raise Exception("Table with display_name %s already exists in repo %s" % (table_display_name,repo))
      if provided_rn:
        rn = provided_rn
      else:
        rn = self.gen_string(table_display_name)
      #Create the metadata for versioned table
      cur.execute(CREATE_VERSIONED_TABLE,(rn, table_display_name, repo))   
      cur.execute(CREATE_VERSIONS_TABLE, (rn,v_id))
      #CLONE table
      log.error("TODO get pk add del bit") #TODO
      if data_con:
        log.info("using exsisting datacon")
        #using an existing data connection
        data_cur = data_con.cursor()
        cloneSQL = CLONE_TABLE_WITH_DATA %( rn, table_display_name)
        data_cur.execute(cloneSQL)
      else:
        cur.execute(CLONE_TABLE_WITH_DATA ,(rn, table_display_name))
      self.connection.commit()
      if data_con:
        data_con.commit()
    except Exception, e:
      log.error(e)
      rn = None
      self.connection.rollback()
      if data_con:
        data_con.rollback()
    cur.close()
      
    return rn    
  #Create a new table associated with a version
  def create_table(self, user, repo, table_display_name, create_sql, v_id, provided_rn = None):
    log.info("Create table display:%s v_id:%s sql: %s " % (table_display_name,v_id, create_sql ))
    rn = None
    cur = self.connection.cursor()
    try:
      #Ensure that no other display name exists in the repo
      cur.execute(GET_TABLE_DISP_COUNT,(table_display_name,repo))
      cnt = cur.fetchone()[0]
      if cnt != 0:
        raise Exception("Table with display_name %s already exists in repo %s" % (table_display_name,repo))
      if provided_rn:
        rn = provided_rn
      else:
        rn = self.gen_string(table_display_name)
      #Create the metadata for versioned table
      cur.execute(CREATE_VERSIONED_TABLE,(rn, table_display_name, repo))   
      cur.execute(CREATE_VERSIONS_TABLE, (rn,v_id))
      #Update create statement
      mod_sql = self.replace_table_name(table_display_name, rn, create_sql)
      mod_sql = self.validate_extend_create_sql(mod_sql)
      #create the db
      cur.execute(mod_sql)
      # add Delete bit
      cur.execute(MOD_TABLE_DH_ATTRS%rn)
      self.connection.commit()
    except Exception, e:
      log.error(e)
      rn = None
      self.connection.rollback()
    cur.close()
    return rn    

  #clone a table 
  def clone_table(self,table_real_name, new_v_id, new_name=None):
    cur = self.connection.cursor()
    try:
      #find the table information for source table
      cur.execute(GET_TABLE,(table_real_name,))
      r = cur.fetchone()
      if new_name:
        rn = new_name
      else:
        rn = self.gen_string(r[1])
      #create the meta data
      cur.execute(CREATE_VERSIONED_TABLE,(rn, r[1], r[2]))
      cur.execute(CREATE_TABLE_PARENT, (rn,table_real_name))   
      #update version pointer for table
      cur.execute(UPDATE_VERSIONS_TABLE, (rn, table_real_name, new_v_id))
      #create a copy of source table
      sql = CLONE_TABLE%(rn, table_real_name)
      cur.execute(sql)
      self.connection.commit()
    except Exception, e:
      log.error(e)
      rn = None
      self.connection.rollback()
    cur.close()
    return rn

#*********Query Commit/Stash/Revert*******************
      
  def get_query_trace(self, v_id1, v_id2):
    #Not needed now
    raise Exception("TODO")




  #UPDATE_USER_HEAD='update table set head_version = %s where user_id = %s and repo= %s'
  #INSERT_USER_HEAD='insert into user_head (user_id, repo, head_version) select %s, %s, %s where not exists (select 1 from user_head user_id = %s and repo = %s'  
  def update_user_head(self, user, repo, v_id, v_name=None):
    log.info("update user head %s %s %s " % (user,repo,v_id))
    res = False      
    cur = self.connection.cursor()
    try:
      #find the table information for source table
      cur.execute(UPDATE_USER_HEAD,(v_id,user,repo))
      cur.execute(INSERT_USER_HEAD,(user,repo,v_id,user,repo))
      self.connection.commit()
      res = True
    except Exception, e:
      log.error(e)
      self.connection.rollback()
    cur.close()
    return res
  
  def stash(self, user, repo, rn, v_id):
    raise Exception("TODO")
  
  def revert(self, user, repo, rn):
    #delete physical table
    #delete meta versioned table
    #delete meta table_parent mapping entry
    #update user head
    raise Exception("TODO")
  
  def commit(self, query_list, v_id):
    #update query log
    #insert into active table of v
    #Not needed now??
    raise Exception("TODO")
