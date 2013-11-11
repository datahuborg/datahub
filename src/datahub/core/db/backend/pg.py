import psycopg2
import re

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub internal APIs for postgres database
'''

class PGBackend:
  def __init__(
      self, user, password, host='localhost', port=5432, db_name=None):

    self.user = user
    self.password = password
    self.host = host
    self.port = port

    if db_name:
      self.connection = psycopg2.connect(
          user=user, password=password, host=host, port=port, database=db_name)
    else:
      self.connection = psycopg2.connect(
          user=user, password=password, host=host, port=port)

    self.connection.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)


  def execute_sql(self, query, params=None):
    result = {
        'status': False,
        'row_count': 0,
        'tuples': [],
        'column_names': [],
        'column_types': []
    }

    conn = self.connection 
    c = conn.cursor()
    c.execute(query.strip(), params)

    try:
      tuples = c.fetchall()
      result['tuples'] = [list(t) for t in tuples]
    except:
      pass

    result['status'] = True
    result['row_count'] = c.rowcount
    if c.description:
      result['column_names'] = [col[0] for col in c.description]

    tokens = query.strip().split(' ', 2)
    c.close()
    return result

  def list_tables(self):
    s = ''' SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' '''

    return self.execute_sql(s);

  '''
  The following methods run in superuser mode
  '''

  def list_databases(self, username):
    s = ''' SELECT datname
        FROM pg_database JOIN pg_authid 
        ON pg_database.datdba = pg_authid.oid
        WHERE rolname = '%s' ''' %(username)

    return self.execute_sql(s)

  def create_user(self, username, password):
    s = ''' CREATE ROLE %s WITH LOGIN
        CREATEDB PASSWORD '%s' 
        ''' %(self.user, self.password)

    return self.execute_sql(s)

  def chnage_password(self, username, password):
    s = ''' ALTER ROLE %s WITH PASSWORD '%s' 
        ''' %(self.user, self.password)

    return self.execute_sql(s)

  def close(self):    
    self.connection.close()


def test():
  backend = PGBackend(user='postgres', password='postgres')
  print  backend.list_databases()

  try:
    backend.execute_sql(''' drop database test ''')
    print  backend.list_databases()
  except:
    pass

  print backend.execute_sql(''' create database test ''')
  print  backend.list_databases()
  backend = PGBackend(user='postgres', password='postgres', db_name='test')
  print backend.list_tables()
  print backend.execute_sql(
      ''' create table person (id integer, name varchar(20)) ''')
  backend = PGBackend(user='postgres', password='postgres', db_name='test')
  print backend.list_tables()
  print backend.execute_sql(''' select * from person ''')
  print backend.execute_sql(''' insert into person values (1, 'anant') ''')
  backend = PGBackend(user='postgres', password='postgres', db_name='test')
  print backend.execute_sql(''' select * from person where id = %s''', (1,))


if __name__ == '__main__':
  test()
