import psycopg2
import re
import csv
import codecs

from config.settings import *

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub internal APIs for postgres database
'''
host = DATABASES['default']['HOST']
port = 5432 if DATABASES['default']['PORT'] == '' else int(DATABASES['default']['PORT'])

class PGBackend:
  def __init__(
      self, user, password, host=host, port=port, db_name=None):

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

  def create_repo(self, repo):
    query = ''' CREATE SCHEMA %s ''' %(repo)
    return self.execute_sql(query)

  def list_repos(self):
    query = ''' SELECT schema_name as repo_name FROM information_schema.schemata
        WHERE schema_owner = '%s' ''' %(self.user)
    return self.execute_sql(query)

  def delete_repo(self, repo, force=False):
    query = ''' DROP SCHEMA %s %s''' %(repo, 'CASCADE' if force else '')
    return self.execute_sql(query)

  def list_tables(self, repo):
    res = self.list_repos()

    all_repos = [t[0] for t in res['tuples']]
    if repo not in all_repos:
      raise LookupError('invalid repository name: %s' %(repo))

    query = ''' SELECT table_name as table FROM information_schema.tables
        WHERE table_schema = '%s' ''' %(repo)
    return self.execute_sql(query)

  def desc_table(self, table):
    tokens = table.split('.')
    if len(tokens) < 2:
      raise NameError (
          "can't resolve the name: '%s'.\n"
          "HINT: use <repo-name>.<table-name> " %(table))
    query = ''' SELECT column_name as field_name, data_type as field_type
        from information_schema.columns
        where table_name = '%s'
        and table_schema = '%s' ''' %(tokens[-1], tokens[-2])
    return self.execute_sql(query)

  def execute_sql(self, query, params=None):
    result = {
        'status': False,
        'row_count': 0,
        'tuples': [],
        'fields': []
    }

    conn = self.connection 
    c = conn.cursor()
    c.execute(query.strip(), params)

    try:
      result['tuples'] = c.fetchall()
    except:
      pass

    result['status'] = True
    result['row_count'] = c.rowcount
    if c.description:
      result['fields'] = [{'name': col[0], 'type': col[1]} for col in c.description]

    tokens = query.strip().split(' ', 2)
    c.close()
    return result

  def create_user(self, username, password):
    query = ''' CREATE ROLE %s WITH LOGIN 
        NOCREATEDB NOCREATEROLE NOCREATEUSER PASSWORD '%s'
        ''' %(username, password)

    return self.execute_sql(query)

  def change_password(self, username, password):
    query = ''' ALTER ROLE %s WITH PASSWORD '%s' 
        ''' %(username, password)

    return self.execute_sql(query)


  def create_table_from_file(path, database, table_name):
    conn = self.connection 
    c = conn.cursor()
    f = codecs.open(path, 'r', 'utf-8')
    data = csv.reader(f)
    cells = data.next()
    columns = map(lambda x: re.sub(r'\W+', '_', x), cells)
    columns = map(lambda x: re.sub(r'\.', '_', x), columns)
    columns = map(lambda x: '_' + x[-20:], columns)
    columns = filter(lambda x: x!='', columns)
    query = 'CREATE TABLE %s (%s text' % (table_name, columns[0])
    for i in range(1, len(columns)):
      query += ', %s %s' %(columns[i], 'text')
    query += ')'
    c.execute(query)

    c.execute("copy %s from '%s' WITH CSV HEADER ENCODING 'ISO-8859-1';" %(table_name, path))
    conn.commit()

  def close(self):    
    self.connection.close()

