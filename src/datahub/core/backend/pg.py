import psycopg2
import re

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub internal APIs for postgres database
'''

kCommitTokens = ['create', 'update', 'alter', 'delete', 'insert', 'drop']

class PGBackend:
  def __init__(
      self, user='postgres', password='postgres',
      host='localhost', port=5432, db_name='postgres'):

    self.connection = psycopg2.connect(
        user=user, password=password, host=host, port=port, database=db_name)

  def execute_sql(self, query, params=None):
    result = {
        'status': False,
        'row_count': 0,
        'tuples': [],
        'column_names': [],
        'column_types': []
    }

    if query.lower().strip().startswith(
        'create database') or query.lower().strip().startswith(
            'drop database'):
      self.connection.set_isolation_level(
          psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    c = self.connection.cursor()
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
    if tokens[0].lower() in kCommitTokens:
      self.connection.commit()

    c.close()
    return result

  def list_databases(self):
    s = ''' SELECT datname FROM pg_catalog.pg_database
        WHERE NOT datistemplate '''

    return self.execute_sql(s)

  def list_tables(self):
    s = ''' SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' '''

    return self.execute_sql(s);

  def close(self):    
    self.connection.close()


def test():
  backend = PGBackend()
  print  backend.list_databases()

  try:
    backend.execute_sql(''' drop database test ''')
    print  backend.list_databases()
  except:
    pass

  print backend.execute_sql(''' create database test ''')
  print  backend.list_databases()
  backend = PGBackend(db_name='test')
  print backend.list_tables()
  print backend.execute_sql(
      ''' create table person (id integer, name varchar(20)) ''')
  backend = PGBackend(db_name='test')
  print backend.list_tables()
  print backend.execute_sql(''' select * from person ''')
  print backend.execute_sql(''' insert into person values (1, 'anant') ''')
  backend = PGBackend(db_name='test')
  print backend.execute_sql(''' select * from person ''')


if __name__ == '__main__':
  test()
