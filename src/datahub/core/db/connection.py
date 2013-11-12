import psycopg2
import re

from backend.pg import PGBackend

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub DB wrapper for backends (only postgres implemented)
'''

class Connection:
  def __init__(self, user, password, db_name=None):
    self.backend = PGBackend(user, password, db_name=db_name)

  def execute_sql(self, query, params=None):
    return self.backend.execute_sql(query, params)

  def list_tables(self, schema):
    return self.backend.list_tables(schema=schema)

  def list_schemas(self):
    return self.backend.list_schemas()

  def close(self):    
    self.backend.close()

  '''
  The following methods run in superuser mode
  '''
  @staticmethod
  def list_databases(username):
    s_backend = PGBackend(user='postgres', password='postgres')
    return s_backend.list_databases(username)

  @staticmethod
  def create_user(username, password):
    s_backend = PGBackend(user='postgres', password='postgres')
    s_backend.execute_sql('create database %s' %(username))
    return s_backend.create_user(username, password)

  @staticmethod
  def change_password(username, password):
    s_backend = PGBackend(user='postgres', password='postgres')
    return s_backend.change_password(username, password)


def test():
  con = Connection(user='postgres', password='postgres')
  print  con.list_databases()

  try:
    print con.execute_sql(''' drop database test ''')
    print  con.list_databases()
  except:
    pass

  print con.execute_sql(''' create database test ''')
  print  con.list_databases()
  con = Connection(user='postgres', password='postgres', db_name='test')
  print con.list_tables()
  print con.execute_sql(
      ''' create table person (id integer, name varchar(20)) ''')
  con = Connection(user='postgres', password='postgres', db_name='test')
  print con.list_tables()
  print con.execute_sql(''' select * from person ''')
  print con.execute_sql(''' insert into person values (1, 'anant') ''')
  con = Connection(user='postgres', password='postgres', db_name='test')
  print con.execute_sql(''' select * from person ''')


if __name__ == '__main__':
  test()
