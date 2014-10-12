import psycopg2
import re

from config import settings

'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub internal APIs for postgres database
'''
HOST = settings.DATABASES['default']['HOST']
PORT = 5432 if settings.DATABASES['default']['PORT'] == '' else int(settings.DATABASES['default']['PORT'])

class PGBackend:
  def __init__(self, user, password, host=HOST, port=PORT, database=None):
    self.user = user
    self.password = password
    self.host = host
    self.port = port
    self.database = database

    self.__open_connection__()

  def __open_connection__(self):    
    self.connection = psycopg2.connect(
        user=self.user,
        password=self.password,
        host=self.host,
        port=self.port,
        database=self.database)

    self.connection.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

  def reset_connection(self, database):
    self.database=database
    self.__open_connection__()

  def close_connection(self):    
    self.connection.close()

  def create_repo(self, repo):
    query = ''' CREATE SCHEMA %s ''' %(repo)
    return self.execute_sql(query)

  def list_repos(self):
    query = ''' SELECT schema_name AS repo_name
                FROM information_schema.schemata
                WHERE schema_owner = '%s'
            ''' %(self.user)
    return self.execute_sql(query)

  def delete_repo(self, repo, force=False):
    query = ''' DROP SCHEMA %s %s
            ''' %(repo, 'CASCADE' if force else '')
    return self.execute_sql(query)

  def share_repo(self, repo, username, privileges, auto_in_future):
    query = ''' GRANT USAGE ON SCHEMA %s TO %s;
            ''' %(repo, username)
    self.execute_sql(query)
    privileges_str = ', '.join(privileges)
    query = ''' GRANT %s ON ALL TABLES
                in SCHEMA %s TO %s;
            ''' %(privileges_str, repo, username)
    self.execute_sql(query)
    query = ''' ALTER DEFAULT PRIVILEGES IN SCHEMA %s
                GRANT %s ON TABLES TO %s;
            ''' %(repo, privileges_str, username)
    self.execute_sql(query)

  def list_tables(self, repo):
    res = self.list_repos()

    all_repos = [t[0] for t in res['tuples']]
    if repo not in all_repos:
      raise LookupError('Invalid repository name: %s' %(repo))

    query = ''' SELECT table_name AS table FROM information_schema.tables
                WHERE table_schema = '%s'
            ''' %(repo)
    return self.execute_sql(query)

  def print_schema(self, table):
    tokens = table.split('.')
    
    if len(tokens) < 2:
      raise NameError (
          "Can't resolve the name: '%s'.\n"
          "HINT: use <repo-name>.<table-name> " %(table))
    
    query = ''' SELECT column_name AS field_name, data_type AS field_type
                FROM information_schema.columns
                WHERE table_name = '%s'
                AND table_schema = '%s'
            ''' %(tokens[-1], tokens[-2])
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
    query = ''' ALTER ROLE %s WITH PASSWORD '%s'
            ''' %(username, password)
    return self.execute_sql(query)

  def list_shared_repos(self, username):
    query = ''' SELECT DISTINCT table_catalog, table_schema
                FROM information_schema.table_privileges
                WHERE grantee='%s'
            ''' %(username)
    return self.execute_sql(query)

  def has_user_access_privilege(self, login, privilege):
    query = ''' SELECT has_database_privilege('%s', '%s')
            ''' %(login, privilege)
    return self.execute_sql(query)

  def has_repo_privilege(self, login, repo, privilege):
    query = ''' SELECT has_schema_privilege('%s', '%s', '%s')
            ''' %(login, repo, privilege)
    return self.execute_sql(query)

  def has_table_privilege(self, login, table, privilege):
    query = ''' SELECT has_table_privilege('%s', '%s', '%s')
            ''' %(login, table, privilege)
    return self.execute_sql(query)

  def has_column_privilege(self, login, table, column, privilege):
    query = ''' SELECT has_column_privilege('%s', '%s', '%s')
            ''' %(login, table, column, privilege)
    return self.execute_sql(query)

  def export_file(self, table_name, file_path, file_format='CSV',
      delimiter=',', header=True):
    header_option = 'HEADER' if header else ''
    return self.execute_sql(
        ''' COPY %s TO '%s'
            WITH %s %s DELIMITER '%s';
        ''' %(table_name, file_path, file_format, header_option, delimiter))

  def import_file(self, table_name, file_path, file_format='CSV',
      delimiter=',', header=True, encoding='ISO-8859-1'):
    try:
      header_option = 'HEADER' if header else ''
      return self.execute_sql(
          ''' COPY %s FROM '%s'
              WITH %s %s DELIMITER '%s' ENCODING '%s';
          ''' %(table_name, file_path, file_format,
                header_option, delimiter, encoding))
    except:
      """
      Try importing using dbtruck.
      """
      return self.import_file_w_dbtruck(table_name, file_path)

  def import_file_w_dbtruck(self, table_name, file_path):
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

    return import_datafiles([file_path], create_new, table_name, errfile,
        PGMethods, **dbsettings)

