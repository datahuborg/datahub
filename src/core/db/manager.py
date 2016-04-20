import six
import hashlib
import os
import errno
import re
import codecs
import csv
from shutil import rmtree

from django.contrib.auth.models import User

from config import settings
from core.db.connection import DataHubConnection
from inventory.models import App, Card, Collaborator, DataHubLegacyUser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class _superuser_connection():
    superuser_con = None

    def __init__(self, repo_base=None):
        self.repo_base = repo_base

    def __enter__(self):
        self.superuser_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            repo_base=self.repo_base)
        return self.superuser_con

    def __exit__(self, type, value, traceback):
        self.superuser_con.close_connection()


class DataHubManager:

    def __init__(self, user=settings.ANONYMOUS_ROLE, repo_base=None,
                 is_app=False):

        # blank users are set to anonymous role
        if user == '':
            user = settings.ANONYMOUS_ROLE

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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close_connection()

    """ Basic Operations. """

    def change_repo_base(self, repo_base):
        """Changes the repo base and resets the DB connection."""
        self.user_con.change_repo_base(repo_base=repo_base)

    def set_search_paths(self, search_paths=[]):
        """
        Sets the search path, so that the user won't have to write
        out schema names.
        """
        return self.user_con.set_search_paths(search_paths)

    def close_connection(self):
        self.user_con.close_connection()

    def create_repo(self, repo):
        return self.user_con.create_repo(repo=repo)

    def list_repos(self):
        return self.user_con.list_repos()

    def rename_repo(self, repo, new_name):
        # only a repo owner can rename a repo:
        if self.repo_base != self.username:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # rename in user_con
        success = self.user_con.rename_repo(repo=repo, new_name=new_name)
        if success:
            # update collaborator(s), if there are any
            Collaborator.objects.filter(
                repo_name=repo, repo_base=self.repo_base).update(
                    repo_name=new_name)

        return success

    def list_collaborator_repos(self):
        """
        Lists repositories that the current user has been granted permission
        to access.

        Note that this method relies on the Collaborators django model. If a
        user bypasses DataHub's api, and grants permissions via the database,
        collaborator repos will not show.
        """
        user = User.objects.get(username=self.username)

        return Collaborator.objects.filter(user=user)

    def delete_repo(self, repo, force=False):
        # Only a repo owner can delete repos.
        if self.repo_base != self.username:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # remove related collaborator objects
        Collaborator.objects.filter(
            repo_name=repo, repo_base=self.repo_base).delete()

        # finally, delete the actual schema
        res = self.user_con.delete_repo(repo=repo, force=force)
        DataHubManager.delete_user_data_folder(self.repo_base, repo)
        return res

    def create_table(self, repo, table, params):
        """Creates a table with the current user/repo_base"""
        return self.user_con.create_table(
            repo=repo, table=table, params=params)

    def list_tables(self, repo):
        return self.user_con.list_tables(repo=repo)

    def describe_table(self, repo, table, detail=False):
        return self.user_con.describe_table(repo, table, detail)

    def list_table_permissions(self, repo, table):
        return self.user_con.list_table_permissions(repo, table)

    def create_view(self, repo, view, sql):
        return self.user_con.create_view(
            repo=repo, view=view, sql=sql)

    def list_views(self, repo):
        return self.user_con.list_views(repo=repo)

    def describe_view(self, repo, view, detail=False):
        return self.user_con.describe_view(repo, view, detail)

    def delete_view(self, repo, view, force=False):
        return self.user_con.delete_view(repo=repo, view=view, force=force)

    def delete_table(self, repo, table, force=False):
        return self.user_con.delete_table(repo=repo, table=table, force=force)

    def get_schema(self, repo, table):
        return self.user_con.get_schema(repo=repo, table=table)

    def explain_query(self, query):
        return self.user_con.explain_query(query)

    def execute_sql(self, query, params=None):
        return self.user_con.execute_sql(query=query, params=params)

    def add_collaborator(
            self, repo, collaborator, db_privileges, file_privileges):
        """
        Grants a user or app privileges on a repo.

        - collaborator must match an existing User's username or an existing
        App's app_id.
        - db_privileges must be an array of SQL privileges as strings.
          e.g. ['SELECT', 'UPDATE', 'INSERT']
        - file_privileges must be an array of file privileges.
          e.g. ['read', 'write']
        """
        # Usage is probably not the right check, but neither is CREATE.
        # The trouble is that roles INHERIT permissions from one another
        # depending on whether that flag was set during creation... and I
        # haven't figured out a way to check on whether a user can grant
        # permission to another without actually doing it.
        # For now, we limit adding_collaborators to the actual owner, who has
        # create privileges
        res = DataHubManager.has_repo_db_privilege(
            self.username, self.repo_base, repo, 'CREATE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # you can't add yourself as a collaborator
        if self.username == collaborator:
            raise Exception(
                "Can't add a repository's owner as a collaborator.")

        try:
            app = App.objects.get(app_id=collaborator)
            collaborator_obj, _ = Collaborator.objects.get_or_create(
                app=app, repo_name=repo, repo_base=self.repo_base)
        except App.DoesNotExist:
            user = User.objects.get(username=collaborator)
            collaborator_obj, _ = Collaborator.objects.get_or_create(
                user=user, repo_name=repo, repo_base=self.repo_base)

        # convert privileges list to string and save the object
        db_privilege_str = ', '.join(db_privileges)
        file_privilege_str = ', '.join(file_privileges).lower()

        collaborator_obj.permission = db_privilege_str
        collaborator_obj.file_permission = file_privilege_str

        collaborator_obj.save()

        return self.user_con.add_collaborator(
            repo=repo,
            collaborator=collaborator,
            db_privileges=db_privileges
        )

    def delete_collaborator(self, repo, collaborator):
        with _superuser_connection(self.repo_base) as conn:
            collaborators = conn.list_collaborators(repo=repo)
            collaborators = [c.get('username') for c in collaborators]

            # The reason we're enforcing permission checks this way is to deal
            # with the edge case where a user removes himself as a collaborator
            # from another user's repo.
            if collaborator not in collaborators:
                raise Exception('Failed to delete collaborator.'
                                ' %s is not a collaborator in the specified'
                                'repository.' % collaborator)
            if (self.username != collaborator and
                    self.username != self.repo_base):
                raise PermissionDenied(
                    'Access denied. Missing required privileges')

            collab = User.objects.get(username=collaborator)
            Collaborator.objects.get(
                user=collab, repo_name=repo, repo_base=self.repo_base).delete()

            result = conn.delete_collaborator(
                repo=repo, collaborator=collaborator)
        return result

    def list_repo_files(self, repo):
        # check for permissions
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'read')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # make a directory for files, if it doesn't already exist
        repo_dir = DataHubManager.create_user_data_folder(self.repo_base, repo)

        uploaded_files = [f for f in os.listdir(repo_dir)]
        return uploaded_files

    def list_repo_cards(self, repo):
        # check for permission
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'read')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges')

        # get the relevant cards
        cards = Card.objects.all().filter(
            repo_base=self.repo_base, repo_name=repo)
        cards = [c.card_name for c in cards]
        return cards

    def list_collaborators(self, repo):
        """
        returns a list of objects with keys 'username' and 'permissions'.
        'permissions' are tied to the database being queried, and left to the
        user to be interpreted. For postgres, see
        http://www.postgresql.org/docs/9.4/static/sql-grant.html
        An example response:
        # [{'username': 'foo_user', 'permissions': 'UC'},
           {'username': 'bar_user', 'permissions': 'U'}]
        """
        # get the database's idea of permissions
        with _superuser_connection(self.repo_base) as conn:
            db_collabs = conn.list_collaborators(repo=repo)

        # merge it with the datahub collaborator model permissions
        usernames = (db_collab['username'] for db_collab in db_collabs)
        dh_collabs = Collaborator.objects.filter(user__username__in=usernames,
                                                 repo_base=self.repo_base,
                                                 repo_name=repo)
        for db_collab in db_collabs:
            db_collab['file_permissions'] = next(
                (dh_collab.file_permission for dh_collab in dh_collabs
                    if dh_collab.user.username == db_collab['username']),
                '')

        return db_collabs

    def save_file(self, repo, data_file):
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'write')
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
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'write')

        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        file_path = user_data_path(self.repo_base, repo, file_name)
        os.remove(file_path)

    def get_file(self, repo, file_name):
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'read')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        file_path = user_data_path(self.repo_base, repo, file_name)
        file = open(file_path).read()
        return file

    def update_card(self, repo, card_name, new_query=None,
                    new_name=None, public=None):
        """
        Updates cards with new name/query/public variables
        """
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'write')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        card = Card.objects.get(
            repo_base=self.repo_base, repo_name=repo, card_name=card_name)
        # update the card
        if new_query is not None:
            # Queries for cards must work
            try:
                self.execute_sql(new_query)
            except Exception:
                raise PermissionDenied(
                    'Either missing required privileges or bad query')
            card.query = new_query
        if new_name is not None:
            if len(new_name) < 1:
                raise ValueError("new_name must be longer than zero "
                                 "characters")
            card.card_name = new_name
        if public is not None:
            if type(public) is not bool:
                raise TypeError("public must be of type bool")
            card.public = public

        card.save()
        return card

    def get_card(self, repo, card_name):
        """
        used to get cards. This goes through manage.py because, it requires
        a check that the user actually has repo access.
        """
        card = Card.objects.get(
            repo_base=self.repo_base, repo_name=repo, card_name=card_name)
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'read')
        if not (res or card.public):
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
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'write')
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
        res = DataHubManager.has_repo_file_privilege(
            self.username, self.repo_base, repo, 'write')
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

    """
    Static methods that don't require permissions
    """

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

    @staticmethod
    def list_public_repos():
        """
        Lists repositories that are accessible by the dh_public user.
        """
        return Collaborator.objects.filter(user__username=settings.PUBLIC_ROLE)

    """
    The following methods run in superuser mode only
    """

    @staticmethod
    def user_exists(username):
        with _superuser_connection() as conn:
            result = conn.user_exists(username)
        return result

    @staticmethod
    def database_exists(db_name):
        with _superuser_connection() as conn:
            result = conn.database_exists(db_name)
        return result

    """ User/Role Management """

    @staticmethod
    def create_user(username, password, create_db=True):
        """Creates a DB role, database, and data folder for a new user."""
        with _superuser_connection() as conn:
            res = conn.create_user(
                username=username, password=password, create_db=create_db)
            DataHubManager.create_user_data_folder(username)
        return res

    @staticmethod
    def create_user_database(username):
        """ create just the database for a user """
        with _superuser_connection() as conn:
            res = conn.create_user_database(username=username)
            DataHubManager.create_user_data_folder(username)
        return res

    @staticmethod
    def _remove_django_user(username):
        # Get the user associated with the username, delete their apps, and
        # then delete the user
        try:
            user = User.objects.get(username=username)
            apps = App.objects.filter(user=user)
            for app in apps:
                app_id = app.app_id
                DataHubManager.remove_app(app_id=app_id)

            Collaborator.objects.filter(user=user).delete()
            user.delete()
        except User.DoesNotExist:
            user = None

        # Do the same thing for legacy users
        try:
            legacy_user = DataHubLegacyUser.objects.get(username=username)
            apps = App.objects.filter(legacy_user=legacy_user)
            for app in apps:
                app_id = app.app_id
                DataHubManager.remove_app(app_id=app_id)
            legacy_user.delete()
        except DataHubLegacyUser.DoesNotExist:
            legacy_user = None

        # Raise a not found exception if this didn't result in any deletions
        if not user and not legacy_user:
            raise User.DoesNotExist()

    @staticmethod
    def remove_user(username, remove_db=True, ignore_missing_user=False):
        # Delete the Django user
        try:
            DataHubManager._remove_django_user(username)
        except User.DoesNotExist as e:
            if not ignore_missing_user:
                raise e

        # Delete the user's db
        if remove_db:
            DataHubManager.remove_database(username)

        # Make a connection, and delete the user's database role
        with _superuser_connection() as conn:
            try:
                # Try the simple case first: delete the user when they have no
                # db permissions left
                result = conn.remove_user(username=username)
            except:
                # Assume the failure was outstanding db permissions. Remove
                # them and try again.
                all_db_list = DataHubManager.list_all_databases()
                for db in all_db_list:
                    DataHubManager.drop_owned_by(username=username,
                                                 repo_base=db)
                result = conn.remove_user(username=username)
        return result

    @staticmethod
    def remove_app(app_id):
        app = App.objects.get(app_id=app_id)
        Collaborator.objects.filter(app=app).delete()
        app.delete()

        with _superuser_connection() as conn:
            conn.remove_user(username=app_id)

    @staticmethod
    def drop_owned_by(username, repo_base):
        with _superuser_connection(repo_base) as conn:
            result = conn.drop_owned_by(username)
        return result

    @staticmethod
    def list_all_users():
        with _superuser_connection() as conn:
            result = conn.list_all_users()
        return result

    @staticmethod
    def list_all_databases():
        """
        lists all user databases. Does not list some,
        like postgres, templates0, templates1, or datahub
        """
        with _superuser_connection() as conn:
            result = conn.list_all_databases()
        return result

    @staticmethod
    def remove_database(repo_base, revoke_collaborators=True):
        collaborators = Collaborator.objects.filter(repo_base=repo_base)
        for collaborator in collaborators:
            collaborator.delete()

        DataHubManager.delete_user_data_folder(repo_base)
        with _superuser_connection() as conn:
            result = conn.remove_database(repo_base, revoke_collaborators)
        return result

    @staticmethod
    def change_password(username, password):
        with _superuser_connection() as conn:
            result = conn.change_password(username=username,
                                          password=password)
        return result

    """ Import/Export Files """

    @staticmethod
    def import_file(username, repo_base, repo, table, file_name,
                    file_format='CSV', delimiter=',', header=True,
                    encoding='ISO-8859-1', quote_character='"'):
        # check for permissions
        delimiter = delimiter.decode('string_escape')

        res = DataHubManager.has_repo_db_privilege(
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
        with _superuser_connection(repo_base) as conn:
            result = conn.import_file(
                table_name=dh_table_name,
                file_path=file_path,
                file_format=file_format,
                delimiter=delimiter,
                header=header,
                encoding=encoding,
                quote_character=quote_character)
        return result

    @staticmethod
    def export_table(username, repo_base, repo, table, file_format='CSV',
                     delimiter=',', header=True):
        """
        Export a table to a CSV file in the same repo.

        Only superusers can execute the copy command, so this function
        passes the username, and verifies user's permissions.
        """
        # clean up names:
        repo_base = clean_str(repo_base, '')
        repo = clean_str(repo, '')
        table = clean_str(table, '')

        # check for permissions
        res = DataHubManager.has_repo_db_privilege(
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
        with _superuser_connection(repo_base) as conn:
            result = conn.export_table(
                table_name=long_table_name,
                file_path=file_path,
                file_format=file_format,
                delimiter=delimiter,
                header=header)
        return result

    @staticmethod
    def export_view(username, repo_base, repo, view, file_format='CSV',
                    delimiter=',', header=True):
        """
        Export a view to a CSV file in the same repo.

        Only superusers can execute the copy command, so this function
        passes the username, and verifies user's permissions.
        """
        # clean up names:
        repo_base = clean_str(repo_base, '')
        repo = clean_str(repo, '')
        view = clean_str(view, '')

        # check for permissions
        res = DataHubManager.has_repo_db_privilege(
            username, repo_base, repo, 'CREATE')
        if not res:
            raise PermissionDenied(
                'Access denied. Missing required privileges.')

        # make the base_repo and repo's folder, if they don't already exist
        DataHubManager.create_user_data_folder(repo_base, repo)

        # define the file path for the new view
        file_name = clean_file_name(view)
        file_path = user_data_path(repo_base, repo, file_name, file_format)

        # format the full view name
        long_view_name = '%s.%s.%s' % (repo_base, repo, view)

        # pass arguments to the connector
        with _superuser_connection(repo_base) as conn:
            result = conn.export_view(
                view_name=long_view_name,
                file_path=file_path,
                file_format=file_format,
                delimiter=delimiter,
                header=header)
        return result

    @staticmethod
    def export_query(repo_base, query, file_path, file_format='CSV',
                     delimiter=',', header=True):
        with _superuser_connection(repo_base) as conn:
            result = conn.export_query(
                query=query,
                file_path=file_path,
                file_format=file_format,
                delimiter=delimiter,
                header=header)
        return result

    """ Access Privilege Checks """

    @staticmethod
    def has_base_privilege(login, repo_base, privilege):
        with _superuser_connection(repo_base) as conn:
            result = conn.has_base_privilege(
                login=login, privilege=privilege)
        return result

    @staticmethod
    def has_repo_db_privilege(login, repo_base, repo, privilege):
        """
        Returns a bool describing whether the bool user has the DATABASE
        privilege passed in the argument. (i.e. Usage)

        Relies on database role management, so this is a pretty straightforward
        call
        """
        repo = repo.lower()
        repo_base = repo_base.lower()
        with _superuser_connection(repo_base) as conn:
            result = conn.has_repo_db_privilege(
                login=login, repo=repo, privilege=privilege)
        return result

    @staticmethod
    def has_repo_file_privilege(login, repo_base, repo, privilege):
        """
        Returns a bool describing whether or not a user has the FILE privilege
        passed in the argument. (i.e. 'read')

        """
        repo = repo.lower()
        repo_base = repo_base.lower()

        # users always have privileges for their own files
        if login == repo_base:
            return True

        # iterate through the collaboratr objects. If the public/default
        # user have the privileges passed, return true
        # The anonymous user is never explicitly shared with, so we don't need
        # to check for that.
        permitted_collaborators = Collaborator.objects.filter(
            repo_base=repo_base,
            repo_name=repo,
            file_permission__contains=privilege,
            user__username__in=[settings.PUBLIC_ROLE, login])
        return next((True for c in permitted_collaborators), False)

    @staticmethod
    def has_table_privilege(login, repo_base, table, privilege):
        """ a straightforward call to the DB, since it manages this """
        with _superuser_connection(repo_base) as conn:
            result = conn.has_table_privilege(
                login=login, table=table, privilege=privilege)
        return result

    @staticmethod
    def has_column_privilege(login, repo_base, table, column, privilege):
        """ a straightforward call to the DB, since it manages this """
        with _superuser_connection(repo_base) as conn:
            result = conn.has_column_privilege(login=login,
                                               table=table,
                                               column=column,
                                               privilege=privilege)
        return result


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
