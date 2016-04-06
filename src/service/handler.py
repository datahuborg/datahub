import hashlib

from core.db.connection import DataHubConnection
from core.db.manager import DataHubManager

from datahub.constants import *
from datahub.account.constants import *

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Handler
'''


def construct_result_set(res):
    tuples = [Tuple(
        cells=[bytes(val) for val in t]) for t in res['tuples']]

    field_names = [bytes(field['name']) for field in res['fields']]
    field_types = [bytes(field['type']) for field in res['fields']]

    return ResultSet(status=res['status'],
                     num_tuples=res['row_count'],
                     num_more_tuples=0,
                     tuples=tuples,
                     field_names=field_names,
                     field_types=field_types)


class DataHubHandler:

    def __init__(self):
        self.sessions = {}
        pass

    def get_version(self):
        return VERSION

    def open_connection(self, con_params):
        try:
            repo_base = con_params.user

            if con_params.repo_base and con_params.repo_base != '':
                repo_base = con_params.repo_base

            user = ''
            is_app = False

            if con_params.user:
                user = con_params.user
                DataHubConnection(
                    user=con_params.user,
                    password=hashlib.sha1(con_params.password).hexdigest(),
                    repo_base=repo_base)
            else:
                user = con_params.app_id
                is_app = True
                DataHubConnection(
                    user=con_params.app_id,
                    password=hashlib.sha1(con_params.app_token).hexdigest(),
                    repo_base=repo_base)

            '''
            res = DataHubManager.has_base_privilege(user, repo_base, 'CONNECT')
            if not (res and res['tuples'][0][0]):
                raise Exception('Access denied. Missing required privileges.')
            '''

            con = Connection(
                user=user,
                is_app=is_app,
                repo_base=repo_base)

            return con
        except Exception as e:
            raise DBException(message=str(e))

    def create_repo(self, con, repo_name):
        try:
            '''
            res = DataHubManager.has_base_privilege(
                con.user, con.repo_base, 'CREATE')
            if not (res and res['tuples'][0][0]):
              raise Exception('Access denied. Missing required privileges.')
            '''
            manager = DataHubManager(
                user=con.user, repo_base=con.repo_base, is_app=con.is_app)
            res = manager.create_repo(repo=repo_name)
            thrift_crazy_result = {'status': res, 'row_count': -1,
                                   'tuples': [], 'fields': []}

            return construct_result_set(thrift_crazy_result)
        except Exception as e:
            raise DBException(message=str(e))

    def list_repos(self, con):
        try:
            '''
            res = DataHubManager.has_base_privilege(
                con.user, con.repo_base, 'CONNECT')
            if not (res and res['tuples'][0][0]):
              raise Exception('Access denied. Missing required privileges.')
            '''
            manager = DataHubManager(
                user=con.user, repo_base=con.repo_base, is_app=con.is_app)
            res = manager.list_repos()

            # prepare dumb thrift stuff
            tuple_list = zip(res)
            length = len(res)
            thrift_crazy_result = {
                'status': True, 'row_count': length,
                'tuples': tuple_list,
                'fields': [{'type': 1043, 'name': 'repo_name'}]
                }

            return construct_result_set(thrift_crazy_result)
        except Exception as e:
            raise DBException(message=str(e))

    def delete_repo(self, con, repo_name, force_if_non_empty):
        try:
            '''
            res = DataHubManager.has_base_privilege(
                con.user, con.repo_base, 'CREATE')
            if not (res and res['tuples'][0][0]):
              raise Exception('Access denied. Missing required privileges.')

            res = DataHubManager.has_repo_privilege(
                con.user, con.repo_base, repo_name, 'CREATE')
            if not (res and res['tuples'][0][0]):
              raise Exception('Access denied. Missing required privileges.')
            '''
            manager = DataHubManager(
                user=con.user, repo_base=con.repo_base, is_app=con.is_app)
            res = manager.delete_repo(repo=repo_name, force=force_if_non_empty)

            thrift_crazy_result = {'status': res, 'row_count': -1,
                                   'tuples': [], 'fields': []}

            return construct_result_set(thrift_crazy_result)
        except Exception as e:
            raise DBException(message=str(e))

    def list_tables(self, con, repo_name):
        try:
            '''
            res = DataHubManager.has_repo_privilege(
                con.user, con.repo_base, repo_name, 'USAGE')
            if not (res and res['tuples'][0][0]):
              raise Exception('Access denied. Missing required privileges.')
            '''
            manager = DataHubManager(
                user=con.user, repo_base=con.repo_base, is_app=con.is_app)
            res = manager.list_tables(repo=repo_name)

            # create the crazy thrift tuple, since this is for consumption from
            # 3rd party apps, and they haven't upgraded to the new list_tables
            # ARC 2015-12-15
            tuple_list = zip(res)
            length = len(res)
            thrift_crazy_result = {
                'status': True, 'row_count': length,
                'tuples': tuple_list,
                'fields': [{'type': 1043, 'name': 'table_name'}]
                }

            return construct_result_set(thrift_crazy_result)
        except Exception as e:
            raise DBException(message=str(e))

    def get_schema(self, con, table_name):
        # this should really accept repo and table name as seperate
        try:
            manager = DataHubManager(
                user=con.user, repo_base=con.repo_base, is_app=con.is_app)

            # thrift isn't upgraded to use seperate repo and tokens yet,
            # so they have to be split here, and then passed to the manager.
            tokens = table_name.split('.')
            repo = tokens[0]
            table = tokens[1]
            res = manager.get_schema(repo=repo, table=table)

            # apps expect get_schema to return in a backwards way. It's made
            # to be backwards here.
            thrift_crazy_result = {
                'status': True, 'row_count': 0, 'tuples': res,
                'fields': [
                    {'type': 1043, 'name': 'column_name'},
                    {'type': 1043, 'name': 'data_type'}]}

            return construct_result_set(thrift_crazy_result)
        except Exception as e:
            raise DBException(message=str(e))

    def execute_sql(self, con, query, query_params=None):
        try:
            manager = DataHubManager(
                user=con.user, repo_base=con.repo_base, is_app=con.is_app)
            res = manager.execute_sql(query=query, params=query_params)
            return construct_result_set(res)
        except Exception as e:
            raise DBException(message=str(e))
