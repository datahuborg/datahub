from backend.pg import PGBackend

'''
DataHub DB wrapper for backends (only postgres implemented)
Any new backend must implement the DataHubConnection interface
'''


class DataHubConnection:

    def __init__(self, user, password, repo_base=None):
        self.backend = PGBackend(user, password, repo_base=repo_base)

    def change_repo_base(self, repo_base):
        self.backend.change_repo_base(repo_base=repo_base)

    def close_connection(self):
        self.backend.close_connection()

    def create_repo(self, repo):
        return self.backend.create_repo(repo=repo)

    def list_repos(self):
        return self.backend.list_repos()

    def rename_repo(self, repo, new_name):
        return self.backend.rename_repo(repo, new_name)

    def delete_repo(self, repo, force=False):
        return self.backend.delete_repo(repo=repo, force=force)

    def add_collaborator(self, repo, collaborator, db_privileges):
        return self.backend.add_collaborator(
            repo=repo,
            collaborator=collaborator,
            db_privileges=db_privileges)

    def delete_collaborator(self, repo, collaborator):
        return self.backend.delete_collaborator(
            repo=repo,
            collaborator=collaborator)

    def create_table(self, repo, table, params):
        return self.backend.create_table(repo=repo, table=table, params=params)

    def list_tables(self, repo):
        return self.backend.list_tables(repo=repo)

    def describe_table(self, repo, table, detail=False):
        return self.backend.describe_table(
            repo=repo, table=table, detail=detail)

    def list_table_permissions(self, repo, table):
        return self.backend.list_table_permissions(
            repo=repo, table=table)

    def create_view(self, repo, view, sql):
        return self.backend.create_view(repo=repo, view=view, sql=sql)

    def list_views(self, repo):
        return self.backend.list_views(repo=repo)

    def describe_view(self, repo, view, detail=False):
        return self.backend.describe_view(
            repo=repo, view=view, detail=detail)

    def delete_view(self, repo, view, force=False):
        return self.backend.delete_view(repo=repo, view=view, force=force)

    def delete_table(self, repo, table, force=False):
        return self.backend.delete_table(repo=repo, table=table, force=force)

    def get_schema(self, repo, table):
        return self.backend.get_schema(repo=repo, table=table)

    def explain_query(self, query):
        return self.backend.explain_query(query=query)

    def limit_and_offset_select_query(self, query, limit, offset):
        return self.backend.limit_and_offset_select_query(
            query=query, limit=limit, offset=offset)

    def select_table_query(self, repo_base, repo, table):
        return self.backend.select_table_query(
            repo_base=repo_base, repo=repo, table=table)

    def execute_sql(self, query, params=None):
        return self.backend.execute_sql(query, params)

    def has_base_privilege(self, login, privilege):
        return self.backend.has_base_privilege(
            login=login, privilege=privilege)

    def has_repo_db_privilege(self, login, repo, privilege):
        return self.backend.has_repo_db_privilege(
            login=login, repo=repo, privilege=privilege)

    def has_table_privilege(self, login, table, privilege):
        return self.backend.has_table_privilege(
            login=login, table=table, privilege=privilege)

    def has_column_privilege(self, login, table, column, privilege):
        return self.backend.has_column_privilege(
            login=login, table=table, column=column, privilege=privilege)

    '''
    The following methods works only in superuser mode
    '''

    def user_exists(self, username):
        return self.backend.user_exists(username)

    def database_exists(self, db_name):
        return self.backend.database_exists(db_name)

    def create_user(self, username, password, create_db):
        return self.backend.create_user(username, password, create_db)

    def remove_user(self, username):
        return self.backend.remove_user(username)

    def create_user_database(self, username):
        return self.backend.create_user_database(username)

    def drop_owned_by(self, username):
        return self.backend.drop_owned_by(username)

    def list_all_users(self):
        return self.backend.list_all_users()

    def list_all_databases(self):
        return self.backend.list_all_databases()

    def remove_database(self, repo_base, revoke_collaborators=True):
        return self.backend.remove_database(repo_base, revoke_collaborators)

    def change_password(self, username, password):
        return self.backend.change_password(username, password)

    def import_file(self, table_name, file_path, file_format='CSV',
                    delimiter=',', header=True, encoding='ISO-8859-1',
                    quote_character='"'):
        return self.backend.import_file(
            table_name=table_name,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter,
            header=header,
            encoding=encoding,
            quote_character=quote_character)

    def export_table(self, table_name, file_path, file_format='CSV',
                     delimiter=',', header=True):
        return self.backend.export_table(
            table_name=table_name,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter)

    def export_view(self, view_name, file_path, file_format='CSV',
                    delimiter=',', header=True):
        return self.backend.export_view(
            view_name=view_name,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter)

    def export_query(self, query, file_path, file_format='CSV',
                     delimiter=',', header=True):
        return self.backend.export_query(
            query=query,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter)

    def list_collaborators(self, repo):
        return self.backend.list_collaborators(repo)

    # Row Level Security Stuff
    def create_security_policy_schema(self):
        return self.backend.create_security_policy_schema()

    def create_security_policy_table(self):
        return self.backend.create_security_policy_table()

    def create_security_policy(self, policy, policy_type, grantee,
                               grantor, repo_base, repo, table):
        return self.backend.create_security_policy(
            policy=policy,
            policy_type=policy_type,
            grantee=grantee,
            grantor=grantor,
            repo_base=repo_base,
            repo=repo,
            table=table)

    def find_security_policies(
            self, repo_base, repo=None, table=None, policy_id=None,
            policy=None, policy_type=None, grantee=None, grantor=None):
        return self.backend.find_security_policies(
            repo_base, repo, table, policy_id, policy, policy_type,
            grantee, grantor)

    def find_all_security_policies(self, username):
        """
        Find all security policies that are granted by or to a username
        """
        return self.backend.find_all_security_policies(username)

    def update_security_policy(self, policy_id, new_policy, new_policy_type,
                               new_grantee):
        return self.backend.update_security_policy(
            policy_id, new_policy, new_policy_type, new_grantee)

    def find_security_policy_by_id(self, policy_id):
        return self.backend.find_security_policy_by_id(policy_id)

    def remove_security_policy(self, policy_id):
        return self.backend.remove_security_policy(policy_id)

    def can_user_access_rls_table(self,
                                  username,
                                  permissions=['SELECT', 'UPDATE', 'INSERT']):
        return self.backend.can_user_access_rls_table(username, permissions)
