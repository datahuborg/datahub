import re
import os
import errno
import shutil
import hashlib
from collections import namedtuple
from uuid import uuid4
import psycopg2
import core.db.query_rewriter
from psycopg2.extensions import AsIs
from psycopg2.pool import ThreadedConnectionPool
from psycopg2 import errorcodes

from core.db.errors import PermissionDenied
from config import settings

"""
DataHub internal APIs for postgres repo_base
"""
HOST = settings.DATABASES['default']['HOST']
PORT = 5432

if settings.DATABASES['default']['PORT'] != '':
    try:
        PORT = int(settings.DATABASES['default']['PORT'])
    except:
        pass

# Maintain a separate db connection pool for each (user, password, database)
# tuple.
connection_pools = {}
PoolKey = namedtuple('PoolKey', 'user, password, repo_base')


def _pool_for_credentials(user, password, repo_base, create_if_missing=True):
    pool_key = PoolKey(user, password, repo_base)
    # Create a new pool if one doesn't exist or if the existing one has been
    # closed. Normally a pool should only be closed during testing, to force
    # all hanging connections to a database to be closed.
    if pool_key not in connection_pools or connection_pools[pool_key].closed:
        if create_if_missing is False:
            return None
        # Maintains at least 1 connection.
        # Raises "PoolError: connection pool exausted" if a thread tries
        # holding onto than 10 connections to a single database.
        connection_pools[pool_key] = ThreadedConnectionPool(
            0,
            10,
            user=user,
            password=password,
            host=HOST,
            port=PORT,
            database=repo_base)
    return connection_pools[pool_key]


def _close_all_connections(repo_base):
    for key, pool in connection_pools.iteritems():
        if repo_base == key.repo_base and not pool.closed:
            pool.closeall()


def _convert_pg_exception(e):
    # Convert some psycopg2 errors into exceptions meaningful to
    # Django.
    if (e.pgcode == errorcodes.INSUFFICIENT_PRIVILEGE):
        raise PermissionDenied()
    if (e.pgcode == errorcodes.INVALID_PARAMETER_VALUE or
            e.pgcode == errorcodes.UNDEFINED_OBJECT):
        raise ValueError("Invalid parameter in query.")
    if e.pgcode == errorcodes.INVALID_SCHEMA_NAME:
        raise LookupError("Repo not found.")
    if e.pgcode == errorcodes.UNDEFINED_TABLE:
        raise LookupError("Table or view not found.")
    if e.pgcode == errorcodes.DUPLICATE_SCHEMA:
        raise ValueError("A repo with that name already exists.")
    if e.pgcode == errorcodes.DUPLICATE_TABLE:
        raise ValueError("A table with that name already exists.")
    raise e


class PGBackend:

    def __init__(self, user, password, host=HOST, port=PORT, repo_base=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.repo_base = repo_base
        self.query_rewriter = core.db.query_rewriter.SQLQueryRewriter(
            self.repo_base, self.user)
        self.connection = None

        self.__open_connection__()

    def __del__(self):
        self.close_connection()

    def __open_connection__(self):
        pool = _pool_for_credentials(self.user, self.password, self.repo_base)
        self.connection = pool.getconn()
        self.connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    def change_repo_base(self, repo_base):
        self.close_connection()
        self.repo_base = repo_base
        self.__open_connection__()

    def close_connection(self):
        pool = _pool_for_credentials(self.user, self.password, self.repo_base,
                                     create_if_missing=False)
        if self.connection and pool and not pool.closed:
            pool.putconn(self.connection, close=True)
            self.connection = None

    def _check_for_injections(self, noun):
        """
        Raises ValueError if the proposed noun is invalid.

        Valid nouns contain only alphanumeric characters and underscores, and
        must not begin or end with an underscore.
        """
        invalid_noun_msg = (
            "Usernames, repo names, and table names may only contain "
            "alphanumeric characters and underscores, must begin with a "
            "letter, and must not begin or end with an underscore."
        )

        regex = r'^(?![\_\d])[\w\_]+(?<![\_])$'
        valid_pattern = re.compile(regex)
        matches = valid_pattern.match(noun)

        if matches is None:
            raise ValueError(invalid_noun_msg)

    def create_repo(self, repo):
        """Creates a postgres schema for the user."""
        self._check_for_injections(repo)

        query = 'CREATE SCHEMA IF NOT EXISTS %s AUTHORIZATION %s'
        params = (AsIs(repo), AsIs(self.user))

        res = self.execute_sql(query, params)
        return res['status']

    def list_repos(self):
        query = ('SELECT schema_name AS repo_name '
                 'FROM information_schema.schemata '
                 'WHERE schema_owner != %s')
        params = (settings.DATABASES['default']['USER'],)
        res = self.execute_sql(query, params)
        return [t[0] for t in res['tuples']]

    def rename_repo(self, repo, new_name):
        self._check_for_injections(repo)
        self._check_for_injections(new_name)

        query = 'ALTER SCHEMA %s RENAME TO %s'
        params = (AsIs(repo), AsIs(new_name))
        res = self.execute_sql(query, params)
        return res['status']

    def delete_repo(self, repo, force=False):
        """Deletes a repo and the folder the user's repo files are in."""
        self._check_for_injections(repo)

        # drop the schema
        query = 'DROP SCHEMA %s %s'
        params = (AsIs(repo), AsIs('CASCADE') if force is True else AsIs(''))
        res = self.execute_sql(query, params)
        return res['status']

    def add_collaborator(self, repo, collaborator, db_privileges=[]):
        # check that all repo names, usernames, and privileges passed aren't
        # sql injections
        self._check_for_injections(repo)
        self._check_for_injections(collaborator)
        for privilege in db_privileges:
            self._check_for_injections(privilege)

        query = ('BEGIN;'
                 'GRANT USAGE ON SCHEMA %s TO %s;'
                 'GRANT %s ON ALL TABLES IN SCHEMA %s TO %s;'
                 'ALTER DEFAULT PRIVILEGES IN SCHEMA %s '
                 'GRANT %s ON TABLES TO %s;'
                 'COMMIT;'
                 )

        privileges_str = ', '.join(db_privileges)
        params = [repo, collaborator, privileges_str, repo,
                  collaborator, repo, privileges_str, collaborator]
        params = tuple(map(lambda x: AsIs(x), params))
        res = self.execute_sql(query, params)
        return res['status']

    def delete_collaborator(self, repo, collaborator):
        self._check_for_injections(repo)
        self._check_for_injections(collaborator)

        query = ('BEGIN;'
                 'REVOKE ALL ON ALL TABLES IN SCHEMA %s FROM %s CASCADE;'
                 'REVOKE ALL ON SCHEMA %s FROM %s CASCADE;'
                 'ALTER DEFAULT PRIVILEGES IN SCHEMA %s '
                 'REVOKE ALL ON TABLES FROM %s;'
                 'COMMIT;'
                 )
        params = [repo, collaborator, repo, collaborator, repo, collaborator]
        params = tuple(map(lambda x: AsIs(x), params))

        res = self.execute_sql(query, params)
        return res['status']

    def create_table(self, repo, table, params):
        # check for injections
        self._check_for_injections(repo)
        self._check_for_injections(table)
        param_values = []
        for obj in params:
            param_values += obj.values()
        for value in param_values:
            self._check_for_injections(value)

        query = ('CREATE TABLE %s.%s (%s)')

        table_params = ''
        for obj in params:
            table_params += obj['column_name']
            table_params += ' '
            table_params += obj['data_type']
            table_params += ', '

        table_params = table_params[:-2]

        params = (AsIs(repo), AsIs(table), AsIs(table_params))
        res = self.execute_sql(query, params)

        return res['status']

    def list_tables(self, repo):
        self._check_for_injections(repo)

        all_repos = self.list_repos()

        if repo not in all_repos:
            raise LookupError('Invalid repository name: %s' % (repo))

        query = ('SELECT table_name FROM information_schema.tables '
                 'WHERE table_schema = %s AND table_type = \'BASE TABLE\';'
                 )
        params = (repo,)
        res = self.execute_sql(query, params)
        return [t[0] for t in res['tuples']]

    def describe_table(self, repo, table, detail=False):
        query = ("SELECT %s "
                 "FROM information_schema.columns "
                 "WHERE table_schema = %s and table_name = %s;")
        params = None
        if detail:
            params = (AsIs('*'), repo, table)
        else:
            params = (AsIs('column_name, data_type'), repo, table)

        res = self.execute_sql(query, params)
        return res['tuples']

    def list_table_permissions(self, repo, table):
        query = ("select privilege_type from "
                 "information_schema.role_table_grants where table_schema=%s "
                 "and table_name=%s and grantee=%s")
        params = (repo, table, self.user)
        res = self.execute_sql(query, params)
        return res['tuples']

    def create_view(self, repo, view, sql):
        self._check_for_injections(repo)
        self._check_for_injections(view)
        query = ('CREATE VIEW %s.%s AS (%s)')

        params = (AsIs(repo), AsIs(view), AsIs(sql))
        res = self.execute_sql(query, params)

        return res['status']

    def list_views(self, repo):
        self._check_for_injections(repo)

        all_repos = self.list_repos()
        if repo not in all_repos:
            raise LookupError('Invalid repository name: %s' % (repo))

        query = ('SELECT table_name FROM information_schema.tables '
                 'WHERE table_schema = %s '
                 'AND table_type = \'VIEW\';')

        params = (repo,)

        res = self.execute_sql(query, params)

        return [t[0] for t in res['tuples']]

    def delete_view(self, repo, view, force=False):
        self._check_for_injections(repo)
        self._check_for_injections(view)

        force_param = 'RESTRICT'
        if force:
            force_param = 'CASCADE'

        query = ('DROP VIEW %s.%s.%s %s')
        params = (AsIs(self.repo_base), AsIs(repo), AsIs(view),
                  AsIs(force_param))

        res = self.execute_sql(query, params)
        return res['status']

    def describe_view(self, repo, view, detail=False):
        query = ("SELECT %s "
                 "FROM information_schema.columns "
                 "WHERE table_schema = %s and table_name = %s;")

        params = None
        if detail:
            params = (AsIs('*'), repo, view)
        else:
            params = (AsIs('column_name, data_type'), repo, view)

        res = self.execute_sql(query, params)

        return res['tuples']

    def delete_table(self, repo, table, force=False):
        self._check_for_injections(repo)
        self._check_for_injections(table)

        force_param = 'RESTRICT'
        if force:
            force_param = 'CASCADE'

        query = ('DROP TABLE %s.%s.%s %s')
        params = (AsIs(self.repo_base), AsIs(repo), AsIs(table),
                  AsIs(force_param))

        res = self.execute_sql(query, params)
        return res['status']

    def get_schema(self, repo, table):
        self._check_for_injections(repo)
        self._check_for_injections(table)

        query = ('SELECT column_name, data_type '
                 'FROM information_schema.columns '
                 'WHERE table_name = %s '
                 'AND table_schema = %s;'
                 )

        params = (table, repo)
        res = self.execute_sql(query, params)

        if res['row_count'] < 1:
            raise NameError("Invalid reference: '%s.%s'.\n" % (repo, table))

        # return will look like [('id', 'integer'), ('words', 'text')]
        return res['tuples']

    def explain_query(self, query):
        """
        returns the number of rows, the cost (in time) to execute,
        and the width (bytes) of rows outputted
        """
        # if it's a select query, return a different set of defaults
        select_query = bool((query.split()[0]).lower() == 'select')

        if not select_query:
            response = {'num_rows': 1, 'time_cost': 0, 'byte_width': 0}
            return response

        query = 'EXPLAIN %s' % (query)
        res = self.execute_sql(query)

        num_rows = re.match(r'.*rows=(\d+).*', res['tuples'][0][0]).group(1)
        byte_width = re.match(r'.*width=(\d+).*', res['tuples'][0][0]).group(1)

        time_cost_re = re.match(
            r'.*cost=(\d+.\d+)..(\d+.\d+)*', res['tuples'][0][0])
        time_cost = (float(time_cost_re.group(1)),
                     float(time_cost_re.group(2)))

        response = {'num_rows': int(num_rows),
                    'time_cost': time_cost,
                    'byte_width': int(byte_width)
                    }
        return response

    def limit_and_offset_select_query(self, query, limit, offset):
        query = query.strip().rstrip(';')

        # is it a select query?
        select_query = False
        if (query.split()[0]).lower() == 'select':
            select_query = True

        # return select query
        if select_query:
            query = ('select * from ( %s ) '
                     'as BXCQWVPEMWVKFBEBNKZSRPYBSB '
                     'LIMIT %s OFFSET %s;'
                     % (query, limit, offset))

        return {'select_query': select_query, 'query': query}

    def select_table_query(self, repo_base, repo, table):
        dh_table_name = '%s.%s.%s' % (repo_base, repo, table)
        query = 'SELECT * FROM %s;' % (dh_table_name)
        return query

    def execute_sql(self, query, params=None, row_level_security=True):
        result = {
            'status': False,
            'row_count': 0,
            'tuples': [],
            'fields': []
        }

        query = query.strip()
        cur = self.connection.cursor()

        try:
            sql_query = cur.mogrify(query, params)
            if row_level_security:
                sql_query = self.query_rewriter.apply_row_level_security(
                    sql_query)
            cur.execute(sql_query)
        except psycopg2.Error as e:
            # Convert some psycopg2 errors into exceptions meaningful to
            # Django.
            _convert_pg_exception(e)

        # if cur.execute() failed, this will print it.
        try:
            result['tuples'] = cur.fetchall()
        except psycopg2.ProgrammingError:
            # print "possible psycopg2.ProgrammingError in pg.execute_sql: "
            # print(e)
            pass

        result['status'] = True
        result['row_count'] = cur.rowcount
        if cur.description:
            result['fields'] = [
                {'name': col[0], 'type': col[1]} for col in cur.description]

        cur.close()
        return result

    def user_exists(self, username):
        query = "SELECT 1 FROM pg_roles WHERE rolname=%s"
        params = (username,)
        result = self.execute_sql(query, params)
        return (result['row_count'] > 0)

    def database_exists(self, db_name):
        query = "SELECT 1 FROM pg_database WHERE datname=%s"
        params = (db_name,)
        result = self.execute_sql(query, params)
        return (result['row_count'] > 0)

    def create_user(self, username, password, create_db=True):
        self._check_for_injections(username)

        query = ('CREATE ROLE %s WITH LOGIN '
                 'NOCREATEDB NOCREATEROLE NOCREATEUSER PASSWORD %s')
        params = (AsIs(username), password)
        self.execute_sql(query, params)

        # Don't do this in the case of the public user.
        if username != settings.PUBLIC_ROLE:
            query = ('GRANT %s to %s')
            params = (AsIs(settings.PUBLIC_ROLE), AsIs(username))
            self.execute_sql(query, params)

        if create_db:
            return self.create_user_database(username)

    def create_user_database(self, username):
        # lines need to be executed seperately because
        # "CREATE DATABASE cannot be executed from a
        # function or multi-command string"
        self._check_for_injections(username)

        query = 'CREATE DATABASE %s; '
        params = (AsIs(username),)
        self.execute_sql(query, params)

        query = 'ALTER DATABASE %s OWNER TO %s; '
        params = (AsIs(username), AsIs(username))
        return self.execute_sql(query, params)

    def remove_user(self, username):
        self._check_for_injections(username)

        query = 'DROP ROLE %s;'
        params = (AsIs(username),)
        return self.execute_sql(query, params)

    def drop_owned_by(self, username):
        self._check_for_injections(username)
        query = 'DROP OWNED BY %s CASCADE;' % (username)
        params = (AsIs(username), )
        return self.execute_sql(query, params)

    def list_all_users(self):
        query = 'SELECT usename FROM pg_catalog.pg_user WHERE usename != %s'
        params = (self.user,)
        res = self.execute_sql(query, params)
        user_tuples = res['tuples']

        all_users_list = []
        for user_tuple in user_tuples:
            all_users_list.append(user_tuple[0])

        return all_users_list

    def list_all_databases(self):
        query = ('SELECT datname FROM pg_database where datname NOT IN '
                 ' (%s, \'template1\', \'template0\', '
                 ' \'datahub\', \'test_datahub\', \'postgres\');'
                 )
        params = (self.user, )
        res = self.execute_sql(query, params)
        db_tuples = res['tuples']

        all_db_list = []
        for db_tuple in db_tuples:
            all_db_list.append(db_tuple[0])

        return all_db_list

    def remove_database(self, database, revoke_collaborators=True):
        self._check_for_injections(database)

        # remove collaborator access to the database
        if revoke_collaborators:
            all_users = self.list_all_users()

            for user in all_users:
                query = "REVOKE ALL ON DATABASE %s FROM %s;"
                params = (AsIs(database), AsIs(user))
                self.execute_sql(query, params)

        # Make sure to close all extant connections to this database or the
        # drop will fail.
        _close_all_connections(database)

        # drop database
        query = 'DROP DATABASE %s;'
        params = (AsIs(database),)
        try:
            return self.execute_sql(query, params)
        except psycopg2.ProgrammingError as e:
                print(e)
                print('this probably happened because the postgres role'
                      'exists, but a database of the same name does not.')

    def change_password(self, username, password):
        self._check_for_injections(username)
        query = 'ALTER ROLE %s WITH PASSWORD %s;'
        params = (AsIs(username), password)
        return self.execute_sql(query, params)

    def list_collaborators(self, repo):
        query = 'SELECT unnest(nspacl) FROM pg_namespace WHERE nspname=%s;'
        params = (repo, )
        res = self.execute_sql(query, params)

        # postgres privileges
        # r -- SELECT ("read")
        # w -- UPDATE ("write")
        # a -- INSERT ("append")
        # d -- DELETE
        # D -- TRUNCATE
        # x -- REFERENCES
        # t -- TRIGGER
        # X -- EXECUTE
        # U -- USAGE
        # C -- CREATE
        # c -- CONNECT
        # T -- TEMPORARY
        # arwdDxt -- ALL PRIVILEGES (for tables, varies for other objects)
        # * -- grant option for preceding privilege
        # /yyyy -- role that granted this privilege

        collaborators = []
        for row in res['tuples']:
            # for reference, rows look like this:
            # ('username=UC/repo_base',)

            collab_obj = {}
            username = row[0].split('=')[0].strip()
            permissions = row[0].split('=')[1].split('/')[0]

            collab_obj['username'] = username
            collab_obj['db_permissions'] = permissions

            collaborators.append(collab_obj)

        return collaborators

    def has_base_privilege(self, login, privilege):
        """
        returns True or False for whether the user has privileges for the
        repo_base (database)
        """
        query = 'SELECT has_database_privilege(%s, %s);'
        params = (login, privilege)
        res = self.execute_sql(query, params)
        return res['tuples'][0][0]

    def has_repo_db_privilege(self, login, repo, privilege):
        """
        returns True or False for whether the use has privileges for the
        repo (schema)
        """
        query = 'SELECT has_schema_privilege(%s, %s, %s);'
        params = (login, repo, privilege)
        res = self.execute_sql(query, params)
        return res['tuples'][0][0]

    def has_table_privilege(self, login, table, privilege):
        query = 'SELECT has_table_privilege(%s, %s, %s);'
        params = (login, table, privilege)
        res = self.execute_sql(query, params)
        return res['tuples'][0][0]

    def has_column_privilege(self, login, table, column, privilege):
        query = 'SELECT has_column_privilege(%s, %s, %s, %s);'
        params = (login, table, column, privilege)
        res = self.execute_sql(query, params)
        return res['tuples'][0][0]

    def export_table(self, table_name, file_path, file_format='CSV',
                     delimiter=',', header=True):
        for word in table_name.split('.'):
            self._check_for_injections(word)

        self._check_for_injections(file_format)

        query = 'SELECT * FROM %s' % table_name
        self.export_query(
            query,
            file_path,
            file_format=file_format,
            delimiter=delimiter,
            header=header)

    def export_view(self, view_name, file_path, file_format='CSV',
                    delimiter=',', header=True):
        for word in view_name.split('.'):
            self._check_for_injections(word)

        self._check_for_injections(file_format)

        query = 'SELECT * FROM %s' % view_name
        self.export_query(
            query,
            file_path,
            file_format=file_format,
            delimiter=delimiter,
            header=header)

    def export_query(self, query, file_path, file_format='CSV',
                     delimiter=',', header=True):
        """
        Runs a query as the current user and saves the result to a file.

        query can be a sql query or table reference.
        """
        header_option = 'HEADER' if header else ''
        query = query.split(';')[0].strip()

        self._check_for_injections(file_format)
        self._check_for_injections(header_option)

        meta_query = 'COPY (%s) TO STDOUT WITH %s %s DELIMITER %s;'
        params = (AsIs(query), AsIs(file_format),
                  AsIs(header_option), delimiter)

        cur = self.connection.cursor()
        query = cur.mogrify(meta_query, params)

        # Store pending exports in a temporary location so they're aren't
        # discoverable while being exported.
        tmp_path = '/tmp/user_exports/{0}-{1}'.format(
            uuid4().hex, hashlib.sha256(query).hexdigest())
        try:
            os.makedirs('/tmp/user_exports')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        try:
            with open(tmp_path, 'w') as f:
                cur.copy_expert(query, f)
        except psycopg2.Error as e:
            # Delete the temporary files of failed exports.
            os.remove(tmp_path)
            _convert_pg_exception(e)
        finally:
            cur.close()
        # Move successful exports into the user's data folder.
        # os.rename() would fail here if /tmp and /user_data are stored on
        # different filesystems, so use shutil.move() instead.
        shutil.move(tmp_path, file_path)

    def import_file(self, table_name, file_path, file_format='CSV',
                    delimiter=',', header=True, encoding='ISO-8859-1',
                    quote_character='"'):

        header_option = 'HEADER' if header else ''

        for word in table_name.split('.'):
            self._check_for_injections(word)
        self._check_for_injections(file_format)
        self._check_for_injections(header_option)

        query = 'COPY %s FROM %s WITH %s %s DELIMITER %s ENCODING %s QUOTE %s;'
        params = (AsIs(table_name), file_path, AsIs(file_format),
                  AsIs(header_option), delimiter, encoding, quote_character)
        try:
            self.execute_sql(query, params, row_level_security=False)
        except Exception as e:
            self.execute_sql('DROP TABLE IF EXISTS %s', (AsIs(table_name),))
            raise ImportError(e)

            # Try importing using dbtruck. Was never enabled by anant.
            # RogerTangos 2015-12-09
            # return self.import_file_w_dbtruck(table_name, file_path)

    def import_file_w_dbtruck(self, table_name, file_path):
        # dbtruck is not tested for safety. At all. It's currently disabled
        # in the project RogerTangos 2015-12-09
        from dbtruck.dbtruck import import_datafiles
        # from dbtruck.util import get_logger
        from dbtruck.exporters.pg import PGMethods

        dbsettings = {
            'dbname': self.repo_base,
            'hostname': self.host,
            'username': self.user,
            'password': self.password,
            'port': self.port,
        }

        create_new = True
        errfile = None

        return import_datafiles([file_path], create_new, table_name, errfile,
                                PGMethods, **dbsettings)

    def _escape_quotes(self, parameter):
        '''
        Replaces single quotes in parameter with double quotes
        to ensure that postgres escapes them.
        '''
        return parameter.replace("'", "''")

    def check_access_permissions(self, grantor, repo_base):
        '''
        Checks if the repo owner is the person granting security policies.
        Only repo owners can create security policies.
        '''
        if (grantor == repo_base or
                grantor == settings.DATABASES['default']['USER']):
            return True
        return False

    def create_security_policy(self, policy, policy_type, grantee, grantor,
                               repo_base, repo, table):
        '''
        Creates a new security policy in the policy table if the policy
        does not yet exist.
        '''
        params = [policy, policy_type, grantee, grantor,
                  table, repo, repo_base]
        params = [self._escape_quotes(param) for param in params]
        for param in params[1:]:
            self._check_for_injections(param)

        if not self.check_access_permissions(grantor, repo_base):
            raise Exception('%s does not have permission to define security '
                            'policies on %s.%s.' % (grantor, repo, table))

        # Raise an exception if the security policy already exists in the table
        security_policy = self.find_security_policy(
            table, repo, repo_base, policy=policy, policy_type=policy_type,
            grantee=grantee, grantor=grantor)

        if security_policy != []:
            raise Exception('Security policy already exists in table.')

        query = ('INSERT INTO dh_public.policy (policy, policy_type, grantee, '
                 'grantor, table_name, repo, repo_base) values '
                 '(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')')
        params = tuple(map(lambda x: AsIs(x), params))

        res = self.execute_sql(query, params, row_level_security=False)

        return res['status']

    def list_security_policies(self, table, repo, repo_base):
        '''
        Return a list of all the security policies defined for the
        specified table.
        '''
        params = [table, repo, repo_base]
        params = [self._escape_quotes(param) for param in params]
        for param in params:
            self._check_for_injections(param)

        query = ('SELECT policy_id, policy, policy_type, grantee, grantor '
                 'FROM dh_public.policy '
                 'WHERE table_name = \'%s\' '
                 'AND repo = \'%s\' AND repo_base = \'%s\'')
        params = tuple(map(lambda x: AsIs(x), params))

        res = self.execute_sql(query, params, row_level_security=False)
        return res['tuples']

    def find_all_security_policies(self, username):
        self._check_for_injections(username)
        params = [username, username]
        query = ('SELECT policy_id, policy, policy_type, grantee, grantor '
                 'FROM dh_public.policy WHERE grantee = \'%s\' or '
                 'grantor = \'%s\'')
        params = tuple(map(lambda x: AsIs(x), params))
        res = self.execute_sql(query, params, row_level_security=False)
        return res['tuples']

    def find_security_policy(self, table_name, repo, repo_base,
                             policy_id=None, policy=None, policy_type=None,
                             grantee=None, grantor=None):
        '''
        Returns a list of all security polices that match the inputs specied
        by the user.
        '''
        params = locals()
        del params["self"]
        query = ('SELECT policy_id, policy, policy_type, grantee, grantor '
                 'FROM dh_public.policy WHERE ')

        first_conditional_added = False
        for key, value in params.items():
            if value is None:
                del params[key]
                continue
            value = self._escape_quotes(value)
            if key != 'policy_id' and key != 'policy':
                self._check_for_injections(str(value))

            if not first_conditional_added:
                query += '%s = \'%s\'' % (key, value)
                first_conditional_added = True
            else:
                query += ' AND %s = \'%s\'' % (key, value)

        res = self.execute_sql(query, row_level_security=False)
        return res['tuples']

    def find_security_policy_by_id(self, policy_id):
        '''
        Returns the security policy that has a policy_id matching the input
        specified by the user.
        '''
        query = ('SELECT policy_id, policy, policy_type, grantee, grantor, '
                 'table_name, repo, repo_base '
                 'FROM dh_public.policy WHERE policy_id = %s' % policy_id)
        res = self.execute_sql(query)
        return res['tuples']

    def update_security_policy(self, policy_id, new_policy, new_policy_type,
                               new_grantee):
        '''
        Updates an existing security policy based on the inputs specified
        by the user.
        '''
        # Need to add quote in front of single quotes to make sure that
        # postgres will escape it
        params = [new_policy, new_policy_type, new_grantee, policy_id]
        params = [self._escape_quotes(param) for param in params]
        self._check_for_injections(params[1])
        self._check_for_injections(params[2])

        policy = self.find_security_policy_by_id(policy_id)
        if policy == []:
            raise LookupError('Policy_ID %s does not exist.' % policy_id)

        if not self.check_access_permissions(policy[0][4], policy[0][7]):
            raise Exception('%s does not have permission to update security '
                            'policies on %s.%s.'
                            % (policy[0][4], policy[0][6], policy[0][5]))

        query = ('UPDATE dh_public.policy '
                 'SET policy = \'%s\', policy_type = \'%s\', '
                 'grantee = \'%s\' '
                 'WHERE policy_id = %s')

        params = tuple(map(lambda x: AsIs(x), params))
        res = self.execute_sql(query, params, row_level_security=False)
        return res['status']

    def remove_security_policy(self, policy_id):
        '''
        Removes the security policy from the policy table with a policy_id
        matching the one specified by the user.
        '''
        policy = self.find_security_policy_by_id(policy_id)
        if policy == []:
            raise LookupError('Policy_ID %s does not exist.' % (policy_id))

        if not self.check_access_permissions(policy[0][4], policy[0][7]):
            raise Exception('%s does not have permission to update security '
                            'policies on %s.%s.'
                            % (policy[0][4], policy[0][6], policy[0][5]))

        query = ('DELETE FROM dh_public.policy WHERE policy_id = %s'
                 % policy_id)
        res = self.execute_sql(query, row_level_security=False)
        return res['status']

    def can_user_access_rls_table(self,
                                  username,
                                  permissions=['SELECT', 'UPDATE', 'INSERT']):
        '''
        Returns True if the has been granted specified type(s) of access to
        select/update/insert into the RLS policy table. Else, returns false.

        This must be executed from a connection to the
        settings.POLICY_DB database. Otherwise, it will check the wrong
        database, and (most likely) return fFalse
        '''
        query = ("SELECT exists("
                 "SELECT * FROM %s.%s where grantee=lower(%s) and (")

        conditions = ["lower(policy_type)=lower(%s)"] * len(permissions)
        conditions = " or ".join(conditions)
        query += conditions + "))"

        params = (AsIs(settings.POLICY_SCHEMA),
                  AsIs(settings.POLICY_TABLE),
                  username) + tuple(permissions)

        res = self.execute_sql(query, params, row_level_security=False)
        return res['tuples'][0][0]
