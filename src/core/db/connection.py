from backend.pg import PGBackend

'''
DataHub DB wrapper for backends (only postgres implemented)
Any new backend must implement the DataHubConnection interface
'''


class DataHubConnection:

    def __init__(self, user, password, repo_base=None):
        self.backend = PGBackend(user, password, repo_base=repo_base)

    def reset_connection(self, repo_base):
        self.backend.reset_connection(repo_base=repo_base)

    def close_connection(self):
        self.backend.close_connection()

    def create_repo(self, repo):
        return self.backend.create_repo(repo=repo)

    def list_repos(self):
        return self.backend.list_repos()

    def delete_repo(self, repo, force=False):
        return self.backend.delete_repo(repo=repo, force=force)

    def add_collaborator(self, repo, username, privileges):
        return self.backend.add_collaborator(
            repo=repo,
            username=username,
            privileges=privileges)

    def delete_collaborator(self, repo, username):
        return self.backend.delete_collaborator(repo=repo, username=username)

    def list_tables(self, repo):
        return self.backend.list_tables(repo=repo)

    def list_views(self, repo):
        return self.backend.list_views(repo=repo)

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

    def has_repo_privilege(self, login, repo, privilege):
        return self.backend.has_repo_privilege(
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

    def remove_user(self, username, remove_db):
        return self.backend.remove_user(username, remove_db)

    def list_all_users(self):
        return self.backend.list_all_users()

    def remove_database(self, username, revoke_collaborators=True):
        return self.backend.remove_database(username, revoke_collaborators)

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
            encoding=encoding,
            quote_character=quote_character)

    def export_table(self, table_name, file_path, file_format='CSV',
                     delimiter=',', header=True):
        return self.backend.export_table(
            table_name=table_name,
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
