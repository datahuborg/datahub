import psycopg2
import re

'''
@author: anant bhardwaj
@date: Oct 3, 2013

datahub connection manager
'''

kCommitTokens = ['create', 'update', 'alter', 'delete', 'insert', 'drop']

class Connection:
  def __init__(self, user="postgres", password="postgres",
               host='localhost', port=5432, db_name='postgres'):
    self.connection = psycopg2.connect(user=user, password=password,
                                      host=host, port=port, database=db_name)

  def __del__(self):
    self.connection.close()

  def execute_sql(self, query, params=None):
    result = {
        'status': False,
        'row_count': 0,
        'tuples': [],
        'column_names': [],
        'column_types': []
    }

    if query.lower().startswith(
        'create database') or query.lower().startswith('drop database'):
      self.connection.set_isolation_level(
          psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    c = self.connection.cursor()
    c.execute(query, params)

    try:
      tuples = c.fetchall()
      for t in tuples:
        result['tuples'].append([str(k) for k in t])
    except:
      pass

    result['status'] = True
    result['row_count'] = c.rowcount
    if c.description:
      result['column_names'] = [col[0] for col in c.description]

    tokens = query.split(' ', 2)
    if tokens[0] in kCommitTokens:
      self.connection.commit()

    c.close()
    return result

  def list_databases(self):
    s = "SELECT datname FROM pg_catalog.pg_database WHERE NOT datistemplate"
    return self.execute_sql(s)

  def list_tables(self):
    s = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
    return self.execute_sql(s);

  def close(self):    
    self.connection.close()


def test():
  con = Connection()
  print  con.list_databases()

  try:
    con.execute_sql('drop database test')
    print  con.list_databases()
  except:
    pass

  con.execute_sql('create database test')
  print  con.list_databases()
  con = Connection(db_name='test')
  print con.list_tables()
  con.execute_sql('create table person(id integer, name varchar(20))')
  print con.list_tables()
  res = con.execute_sql('select * from person')
  print res
  con = Connection(db_name='test')
  res = con.execute_sql("insert into person values(1, 'anant')")
  print res
  con = Connection(db_name='test')
  res = con.execute_sql('select * from person')
  print res


if __name__ == '__main__':
  test()