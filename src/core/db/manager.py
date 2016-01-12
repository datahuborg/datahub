from config import settings
from core.db.connection import DataHubConnection
from inventory.models import App, Card, Collaborator
from django.contrib.auth.models import User

import six
import hashlib
import os
import errno
import re
import codecs
import csv
from shutil import rmtree
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class DataHubManager:

    def __init__(self, user, repo_base=None, is_app=False):
        username = None
        password = None

        if is_app:
            app = App.objects.get(app_id=user)
            username = app.app_id
            password = hashlib.sha1(app.app_token).hexdigest()
        else:
            user = User.objects.get(username=user)
            username = user.username
            password = user.password

        if not repo_base:
            repo_base = username

        self.username = username
        self.repo_base = repo_base

        self.user_con = DataHubConnection(
            user=username,
            repo_base=repo_base,
            password=password)

    ''' Basic Operations. '''

    def change_repo_base(self, repo_base):
        """Changes the repo base and resets the DB connection."""
        self.user_con.change_repo_base(repo_base=repo_base)

    def close_connection(self):
        self.user_con.close()

    def create_repo(self, repo):
        return self.user_con.create_repo(repo=repo)

    def list_repos(self):
        return self.user_con.list_repos()

    def list_collaborator_repos(self):
        user = User.objects.get(username=self.username)
        return Collaborator.objects.filter(user=user)

    def delete_repo(self, repo, force=False):
        # Only a repo owner can delete repos.
        if self.repo_base != self.username:
            raise PermissionDenied(
                'Access denied. Missing required privileges')
        res = self.user_con.delete_repo(repo=repo, force=force)
        DataHubManager.delete_user_data_folder(self.repo_base, repo)
        return res

    def list_tables(self, repo):
        return self.user_con.list_tables(repo=repo)

    def list_views(self, repo):
        return self.user_con.list_views(repo=repo)

    def delete_table(self, repo, table, force=False):
        return self.user_con.delete_table(repo=repo, table=table, force=force)

    def get_schema(self, repo, table):
        return self.user_con.get_schema(repo=repo, table=table)

    def explain_query(self, query):
        return self.user_con.explain_query(query)

    def execute_sql(self, query, params=None):
        return self.user_con.execute_sql(query=query, params=params)

    def add_collaborator(self, repo, username, privileges):
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        user = User.objects.get(username=username)
        Collaborator.objects.create(user=user, repo_name=repo, repo_owner=self.repo_base, permission="ALL")

        return self.user_con.add_collaborator(
            repo=repo,
            username=username,
            privileges=privileges
        )

    def delete_collaborator(self, repo, collaborator):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=self.repo_base)
        repo_collaborators = superuser_con.list_collaborators(repo=repo)

        # The reason we're enforcing permission checks this way is to deal with the edge case 
        # where a user removes himself as a collaborator from another user's repo. 
        if collaborator not in repo_collaborators:
            raise Exception('Failed to delete collaborator. %s is not a collaborator in the specified repository.' % collaborator)
        if self.username != collaborator and self.username != self.repo_base:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        collab = User.objects.get(username=collaborator)
        Collaborator.objects.get(user=collab, repo_name=repo, repo_owner=self.repo_base).delete()
        return superuser_con.delete_collaborator(repo=repo, username=collaborator)
        

    def list_repo_files(self, repo):
        # check for permissions
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # make a directory for files, if it doesn't already exist
        repo_dir = DataHubManager.create_user_data_folder(self.repo_base, repo)

        uploaded_files = [f for f in os.listdir(repo_dir)]
        return uploaded_files

    def list_repo_cards(self, repo):
        # check for permission
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # get the relevant cards
        cards = Card.objects.all().filter(
            repo_base=self.repo_base, repo_name=repo)
        cards = [c.card_name for c in cards]
        return cards

    def list_collaborators(self, repo):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=self.repo_base)
        return superuser_con.list_collaborators(repo=repo)

    def save_file(self, repo, data_file):
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        DataHubManager.create_user_data_folder(self.repo_base, repo)

        file_name = clean_file_name(data_file.name)
        file_path = user_data_path(self.repo_base, repo, file_name)
        with open(file_path, 'wb+') as destination:
            for chunk in data_file.chunks():
                destination.write(chunk)

    def delete_file(self, repo, file_name):
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')

        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        file_path = user_data_path(self.repo_base, repo, file_name)
        os.remove(file_path)

    def get_file(self, repo, file_name):
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        file_path = user_data_path(self.repo_base, repo, file_name)
        file = open(file_path).read()
        return file

    def get_card(self, repo, card_name):
        '''
        used to get cards. This goes through manage.py because, it requires
        a check that the user actually has repo access.
        '''
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        card = Card.objects.get(
            repo_base=self.repo_base, repo_name=repo, card_name=card_name)

        return card

    def create_card(self, repo, query, card_name):
        # to create a card, the user must be able to successfully execute
        # the query from their own database user.
        try:
            self.execute_sql(query)
        except Exception:
            raise PermissionDenied(
                'Either missing required privileges or bad query')

        card, created = Card.objects.get_or_create(
            repo_base=self.repo_base, repo_name=repo,
            card_name=card_name, query=query)

        return card

    def export_card(self, repo, card_name, file_format='CSV'):
        card = Card.objects.get(repo_base=self.repo_base,
                                repo_name=repo, card_name=card_name)
        query = card.query

        # to export a card, the user must be able to successfully execute
        # the query from their own database user.
        try:
            self.execute_sql(query)
        except Exception:
            raise PermissionDenied(
                'Either missing required privileges or bad query')

        # check that they really do have permissions on the repo base.
        # This is a bit paranoid, but only because I don't like giving users
        # superuser privileges
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        # create the repo if it doesn't already exist
        DataHubManager.create_user_data_folder(self.repo_base, repo)

        file_name = clean_file_name(card_name)
        file_path = user_data_path(
            self.repo_base, repo, file_name, file_format)
        DataHubManager.export_query(repo_base=self.repo_base, query=query,
                                    file_path=file_path,
                                    file_format=file_format)

    def delete_card(self, repo, card_name):
        res = DataHubManager.has_repo_privilege(
            self.username, self.repo_base, repo, 'USAGE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        card = Card.objects.get(repo_base=self.repo_base,
                                repo_name=repo, card_name=card_name)
        return card.delete()

    def limit_and_offset_select_query(self, query, limit, offset):
        """
        Modifies select queries, adding limits and offsets.

        Used primarily for pagination
        """
        return self.user_con.limit_and_offset_select_query(
            query=query, limit=limit, offset=offset)

    def paginate_query(self, query, current_page, rows_per_page):
        """
        Set variables for query pagination, limiting query statement
        to just the section of the table that will be displayed
        """
        explanation = self.explain_query(query)

        num_rows = explanation['num_rows']
        time_cost = explanation['time_cost']
        byte_width = explanation['byte_width']
        total_pages = 1 + (num_rows / rows_per_page)

        # set first page that a user can navigate to
        start_page = current_page - 5
        if start_page < 1:
            start_page = 1

        # set the last page that a user can navigate to
        end_page = start_page + 10
        if end_page > total_pages:
            end_page = total_pages

        # set the offset
        offset = (current_page - 1) * rows_per_page

        # add limit and offset for select queries
        res = self.limit_and_offset_select_query(
            query=query, limit=rows_per_page, offset=offset)
        select_query = res['select_query']
        query = res['query']

        # actually make the query
        column_names = None  # top columns
        rows = None  # in tuple form

        res = self.execute_sql(query)

        # determine the column_names and rows
        if select_query or res['row_count'] > 0:  # normal case
            column_names = [field['name'] for field in res['fields']]
            rows = res['tuples']
        else:  # query just returned a bool
            column_names = ['status']
            rows = [['success' if res['status'] else res['error']]]

        result = {
                'num_rows': num_rows,
                'time_cost': time_cost,
                'byte_width': byte_width,
                'total_pages': total_pages,
                'start_page': start_page,
                'end_page': end_page,
                'column_names': column_names,
                'rows': rows,
                'select_query': select_query
        }

        return result

    def select_table_query(self, repo, table):
        """
        Return a database query for selecting the table.

        Necessary for keeping sq/nosql queries out of views.
        """
        return self.user_con.select_table_query(
            repo_base=self.repo_base, repo=repo, table=table)

    '''
    Static methods that don't require permissions
    '''

    @staticmethod
    def create_user_data_folder(repo_base, repo=''):
        """
        Creates a user data folder for the given user.

        Optionally accepts a specific repo's folder to create.
        Fails silently if the folder already exists.
        Returns the deleted path.
        """
        repo_dir = os.path.abspath(
            os.path.join(os.sep, 'user_data', repo_base, repo))
        try:
            os.makedirs(repo_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return repo_dir

    @staticmethod
    def delete_user_data_folder(repo_base, repo=''):
        """
        Deletes a user data folder for the given user.

        Optionally accepts a specific repo's folder to delete.
        Fails silently if the folder does not exist.
        Returns the deleted path.
        """
        repo_dir = os.path.abspath(
            os.path.join(os.sep, 'user_data', repo_base, repo))
        try:
            rmtree(repo_dir)
        except OSError as e:
            if e.errno:
                pass
        return repo_dir

    @staticmethod
    def user_data_folder_exists(username):
        """Returns true if user has a folder in /user_data. False otherwise."""
        repo_dir = os.path.abspath(
            os.path.join(os.sep, 'user_data', username))
        return os.path.exists(repo_dir)

    '''
    The following methods run in superuser mode only
    '''

    @staticmethod
    def user_exists(username):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.user_exists(username)

    @staticmethod
    def database_exists(db_name):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.database_exists(db_name)

    ''' User/Role Management '''

    @staticmethod
    def create_user(username, password, create_db=True):
        """Creates a DB role, database, and data folder for a new user."""
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        res = superuser_con.create_user(
            username=username, password=password, create_db=create_db)
        DataHubManager.create_user_data_folder(username)
        return res

    @staticmethod
    def remove_user(username, remove_db=True):
        if remove_db:
            DataHubManager.remove_database(username)

        all_db_list = DataHubManager.list_all_databases()
        for db in all_db_list:
            DataHubManager.drop_owned_by(username=username, repo_base=db)

        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.remove_user(username=username)

    @staticmethod
    def drop_owned_by(username, repo_base):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.drop_owned_by(username)

    @staticmethod
    def list_all_users():
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.list_all_users()

    @staticmethod
    def list_all_databases():
        '''
        lists all user databases. Does not list some,
        like postgres, templates0, templates1, or datahub
        '''
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.list_all_databases()

    @staticmethod
    def remove_database(repo_name, revoke_collaborators=True):
        DataHubManager.delete_user_data_folder(repo_name)
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.remove_database(repo_name, revoke_collaborators)

    @staticmethod
    def change_password(username, password):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'])
        return superuser_con.change_password(username=username,
                                             password=password)

    ''' Import/Export Files '''

    @staticmethod
    def import_file(username, repo_base, repo, table, file_name,
                    file_format='CSV', delimiter=',', header=True,
                    encoding='ISO-8859-1', quote_character='"'):
        # check for permissions
        delimiter = delimiter.decode('string_escape')

        res = DataHubManager.has_repo_privilege(
            username, repo_base, repo, 'CREATE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        # prepare some variables
        file_path = user_data_path(repo_base, repo, file_name)
        table_name, _ = os.path.splitext(file_name)
        table_name = clean_str(table_name, 'table')
        dh_table_name = '%s.%s.%s' % (repo_base, repo, table_name)

        # open the file
        f = codecs.open(file_path, 'r', 'ISO-8859-1')
        data = csv.reader(f, delimiter=delimiter)

        # create a table for the data
        cells = data.next()
        columns = [clean_str(str(i), 'col') for i in range(0, len(cells))]
        if header:
            columns = map(lambda x: clean_str(x, 'col'), cells)
        columns = rename_duplicates(columns)

        query = 'CREATE TABLE %s (%s text' % (dh_table_name, columns[0])
        for column in columns[1:len(columns)]:
            query += ', %s %s' % (column, 'text')
        query += ')'

        manager = DataHubManager(user=username, repo_base=repo_base)
        manager.execute_sql(query=query)

        # populate the newly created table with data from the csv
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.import_file(
            table_name=dh_table_name,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter,
            header=header,
            encoding=encoding,
            quote_character=quote_character)

    @staticmethod
    def export_table(username, repo_base, repo, table, file_format='CSV',
                     delimiter=',', header=True):
        """
        Export a table to a CSV file in the same repo.

        Only superusers can execute the copy command, so this function
        passes the username, and verifies user's permissions.
        """
        # check for permissions
        res = DataHubManager.has_repo_privilege(
            username, repo_base, repo, 'CREATE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        # make the base_repo and repo's folder, if they don't already exist
        DataHubManager.create_user_data_folder(repo_base, repo)

        # define the file path for the new table
        file_name = clean_file_name(table)
        file_path = user_data_path(repo_base, repo, file_name, file_format)

        # format the full table name
        long_table_name = '%s.%s.%s' % (repo_base, repo, table)

        # pass arguments to the connector
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.export_table(
            table_name=long_table_name,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter,
            header=header)

    @staticmethod
    def export_query(repo_base, query, file_path, file_format='CSV',
                     delimiter=',', header=True):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.export_query(
            query=query,
            file_path=file_path,
            file_format=file_format,
            delimiter=delimiter,
            header=header)

    ''' Access Privilege Checks '''

    @staticmethod
    def has_base_privilege(login, repo_base, privilege):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.has_base_privilege(
            login=login, privilege=privilege)

    @staticmethod
    def has_repo_privilege(login, repo_base, repo, privilege):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.has_repo_privilege(
            login=login, repo=repo, privilege=privilege)

    @staticmethod
    def has_table_privilege(login, repo_base, table, privilege):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.has_table_privilege(
            login=login, table=table, privilege=privilege)

    @staticmethod
    def has_column_privilege(login, repo_base, table, column, privilege):
        superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base=repo_base)
        return superuser_con.has_column_privilege(login=login,
                                                  table=table,
                                                  column=column,
                                                  privilege=privilege)


class PermissionDenied(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def user_data_path(repo_base, repo=None, file_name=None, file_format=None):
    """
    Returns an absolute path to a file or repo in a user's data folder.

    user_data_path('foo') => '/user_data/foo'
    user_data_path('foo', repo='bar') => '/user_data/foo/bar'
    user_data_path('foo', repo='bar', file_name='baz')
        => '/user_data/foo/bar/baz'
    """
    if file_name and not repo:
        raise ValueError('Must pass in repo when providing file_name.')
    parts = [repo_base, repo, file_name]
    for p in parts:
        if (isinstance(p, six.string_types) and
                (len(p) == 0 or p.startswith('.'))):
            raise ValueError('Invalid path component.')
    parts = [repo_base, repo or '', file_name or '']
    path = os.path.abspath(os.path.join(os.sep, 'user_data', *parts))

    if file_format:
        if re.match('[^0-9a-zA-Z_-]', file_format):
            raise ValueError('Invalid file format specified.')
        path = '%s.%s' % (path, file_format)

    return path


def clean_file_name(text):
    # remove leading periods
    return re.sub('^\.+', '', text)


def clean_str(text, prefix):
    string = text.strip().lower()

    # replace whitespace with '_'
    string = re.sub(' ', '_', string)

    # remove invalid characters
    string = re.sub('[^0-9a-zA-Z_]', '', string)

    # remove leading characters until a letter or underscore
    string = re.sub('^[^a-zA-Z_]+', '', string)

    if string == '':
        return clean_str(prefix + text, '')

    return string


def rename_duplicates(columns):
    columns = [c.lower() for c in columns]
    new_columns = []
    col_idx = {c: 1 for c in columns}

    for c in columns:
        if columns.count(c) == 1:
            new_columns.append(c)
        else:
            # add a suffix
            new_columns.append(c + str(col_idx[c]))
            col_idx[c] += 1

    return new_columns
