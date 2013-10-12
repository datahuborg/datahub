import psycopg2
import re

from backend.pg import PGBackend

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub DB wrapper for backends (only postgres implemented)
'''

class Connection:
  def __init__(self, db_name=None):
    self.backend = PGBackend(db_name=db_name)

  def execute_sql(self, query, params=None):
    return self.backend.execute_sql(query, params)

  def list_databases(self):
    return self.backend.list_databases()

  def list_tables(self):
    return self.backend.list_tables()

  def close(self):    
    self.backend.clos()


def test():
  con = Connection()
  print  con.list_databases()

  try:
    print con.execute_sql(''' drop database test ''')
    print  con.list_databases()
  except:
    pass

  print con.execute_sql(''' create database test ''')
  print  con.list_databases()
  con = Connection(db_name='test')
  print con.list_tables()
  print con.execute_sql(
      ''' create table person (id integer, name varchar(20)) ''')
  con = Connection(db_name='test')
  print con.list_tables()
  print con.execute_sql(''' select * from person ''')
  print con.execute_sql(''' insert into person values (1, 'anant') ''')
  con = Connection(db_name='test')
  print con.execute_sql(''' select * from person ''')


if __name__ == '__main__':
  test()