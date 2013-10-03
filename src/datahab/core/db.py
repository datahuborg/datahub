import psycopg2
import re

'''
@author: anant bhardwaj
@date: Oct 3, 2013

datahub connection manager
'''

class Connection:
  def __init__(self, user="postgres", password="postgres", host='localhost', port=5432, db_name='postgres'):
    self.connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=db_name)

  def __del__(self):
    self.connection.close()

  def execute_query(self, sql, params=None):
    res={'status':False}
    c = self.connection.cursor()
    c.execute(sql, params)
    res['data'] = c.fetchall()
    c.close()
    res['status'] = True
    return res

  def list_databases(self):
    s = "SELECT datname FROM pg_catalog.pg_database WHERE NOT datistemplate"
    return self.execute_query(s)

  def list_tables(self):
    s = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    return self.execute_query(s);

  def create_database(self, db_name):
    res={'status':False}
    self.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    c = self.connection.cursor()
    s = "CREATE DATABASE %s" %(db_name)
    c.execute(s, None)
    res={'status':True}
    return res

  def create_table(self, table_name):
    res={'status':False}
    c = self.connection.cursor()             
    s = "CREATE TABLE %s (id int)" %(table_name)
    c.execute(s, None)
    res={'status':True}
    return res

  def close(self):
    self.connection.close()


if __name__ == '__main__':
  con = Connection()
  print  con.list_databases()
  print con.list_tables()
