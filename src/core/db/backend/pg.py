import psycopg2
import re
import csv
import codecs

from config import settings

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub internal APIs for postgres database
'''
host = settings.DATABASES['default']['HOST']
port = 5432 if settings.DATABASES['default']['PORT'] == '' else int(settings.DATABASES['default']['PORT'])

class PGBackend:
  def __init__(
      self, user, password, host=host, port=port, database=None):

    self.user = user
    self.password = password
    self.host = host
    self.port = port
    self.database = database

    if database:
      self.connection = psycopg2.connect(
          user=user, password=password, host=host, port=port, database=database)
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
      result['fields'] = [
          {'name': col[0], 'type': col[1]} for col in c.description]

    tokens = query.strip().split(' ', 2)
    c.close()
    return result

  def create_user(self, username, password):
    query = ''' CREATE ROLE %s WITH LOGIN 
                NOCREATEDB NOCREATEROLE NOCREATEUSER PASSWORD '%s'
                ''' %(username, password)
    self.execute_sql(query)
    query = ''' CREATE DATABASE %s WITH OWNER=%s ''' %(username, username)
    return self.execute_sql(query)

  def change_password(self, username, password):
    query = ''' ALTER ROLE %s WITH PASSWORD '%s' ''' %(username, password)
    return self.execute_sql(query)

  def list_shared_repo(self, username):
    query = ''' SELECT DISTINCT table_catalog, table_schema
                FROM information_schema.table_privileges
                WHERE grantee='%s' ''' %(username)
    return self.execute_sql(query)

  def has_database_privilege(self, username, database, privilege):
    query = ''' SELECT has_database_privilege('%s', '%s', '%s')
                ''' %(username, database, privilege)
    return self.execute_sql(query)

  def has_repo_privilege(self, username, repo, privilege):
    query = ''' SELECT has_schema_privilege('%s', '%s', '%s')
                ''' %(username, repo, privilege)
    return self.execute_sql(query)

  def has_table_privilege(self, username, table, privilege):
    query = ''' SELECT has_table_privilege('%s', '%s', '%s')
                ''' %(username, table, privilege)
    return self.execute_sql(query)

  def has_column_privilege(self, username, table, column, privilege):
    query = ''' SELECT has_column_privilege('%s', '%s', '%s')
                ''' %(username, table, column, privilege)
    return self.execute_sql(query)

  def create_table_from_file(self, path, table_name):
    """
    Try importing using dbtruck.  If it fails for any reason at all,
    then fall back to default COPY import
    """
    try:
      return self.execute_sql(
          "COPY %s FROM '%s' WITH CSV HEADER ENCODING 'ISO-8859-1';" %(
              table_name, path))
    except:
      return self.create_table_from_file_w_dbtruck(path, table_name)

  def create_table_from_file_w_dbtruck(self, path, table_name):
    from dbtruck.dbtruck import import_datafiles
    from dbtruck.util import get_logger
    from dbtruck.exporters.pg import PGMethods

    dbsettings = {
      'dbname': self.database,
      'hostname': self.host,
      'username': self.user,
      'password': self.password,
      'port': self.port,
    }
    
    create_new = True
    errfile = None

    return import_datafiles([path], create_new, table_name, errfile, PGMethods,
                    **dbsettings)

  def close(self):    
    self.connection.close()

