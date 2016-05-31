from rest_framework import serializers

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from inventory.models import Collaborator
from core.db.manager import DataHubManager
from core.db.rlsmanager import RowLevelSecurityManager


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_login', 'email')


class DataHubSerializer(object):

    def __init__(self, username, repo_base, request=None, manager=None):
        self.username = username
        self.repo_base = repo_base
        self.request = request

        # In rare cases, the manager does not need to be instantiated
        # i.e. when listing public repos, which is done via a static method
        try:
            # Reuse an existing manager if one was passed in, to minimize the
            # number of concurrent db connections.
            self.manager = manager or DataHubManager(
                user=self.username, repo_base=self.repo_base)
        except Exception:
            pass

        self.base_uri = ''
        if request:
            self.base_uri = request.build_absolute_uri('/')[:-1]


class RepoSerializer(DataHubSerializer):

    def create_repo(self, repo_name):
        success = self.manager.create_repo(repo_name)
        return success

    def delete_repo(self, repo_name, force=True):
        success = self.manager.delete_repo(repo=repo_name, force=force)
        return success

    def describe_repo(self, repo_name):

        description = {}

        # add owner to description
        owner = {'username': self.repo_base}
        description["owner"] = owner

        # get collaborators
        collaborator_serializer = CollaboratorSerializer(
            username=self.username, repo_base=self.repo_base,
            request=self.request, manager=self.manager)
        collaborators = collaborator_serializer.list_collaborators(repo_name)
        description["collaborators"] = collaborators["collaborators"]

        # get tables
        table_serializer = TableSerializer(
            username=self.username, repo_base=self.repo_base,
            request=self.request, manager=self.manager)
        tables = table_serializer.list_tables(repo_name)
        description["tables"] = tables["tables"]

        # get views
        view_serializer = ViewSerializer(
            username=self.username, repo_base=self.repo_base,
            request=self.request, manager=self.manager)
        views = view_serializer.list_views(repo_name)
        description["views"] = views["views"]

        # get cards
        card_serializer = CardSerializer(
            username=self.username, repo_base=self.repo_base,
            request=self.request, manager=self.manager)
        cards = card_serializer.list_cards(repo_name)
        description["cards"] = cards["cards"]

        # get files
        file_serializer = FileSerializer(
            username=self.username, repo_base=self.repo_base,
            request=self.request, manager=self.manager)
        files = file_serializer.list_files(repo_name)
        description["files"] = files["files"]

        return description

    def rename_repo(self, repo, new_name):
        success = self.manager.rename_repo(repo=repo, new_name=new_name)
        return success

    def user_owned_repos(self):
        repos = self.manager.list_repos()
        repos.sort()
        repo_obj_list = []
        for repo in repos:
            relative_uri = reverse('api:repo', args=(
                self.repo_base, repo))
            absolute_uri = self.base_uri + relative_uri

            repo_obj_list.append({
                'repo_name': repo,
                'href': absolute_uri,
                'owner': self.repo_base
                })

        return {'repos': repo_obj_list}

    def user_accessible_repos(self):
        user_owned_list = self.user_owned_repos()['repos']
        all_collab_list = self.all_collab_repos()['repos']
        return {'repos': user_owned_list + all_collab_list}

    def specific_collab_repos(self, collab_username):
        # get the collaborators
        user = User.objects.get(username=self.username)
        collab_repos = Collaborator.objects.filter(
            user=user, repo_base=collab_username)

        # Either the repo_base doesn't exist, or the current user isn't allowed
        # to see that it exists.
        if len(collab_repos) == 0:
            raise LookupError()

        repo_obj_list = []
        for repo in collab_repos:
            relative_uri = reverse('api:repo', args=(
                self.repo_base, repo.repo_name))
            absolute_uri = self.base_uri + relative_uri

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'href': absolute_uri,
                'owner': repo.repo_base,
                })

        return {'repos': repo_obj_list}

    def public_repos(self):
        public_repos = DataHubManager.list_public_repos()

        repo_obj_list = []
        for repo in public_repos:
            relative_uri = reverse('api:repo', args=(
                repo.repo_base, repo.repo_name))
            absolute_uri = self.base_uri + relative_uri

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'href': absolute_uri,
                'owner': repo.repo_base,
                })

        return {'repos': repo_obj_list}

    def all_collab_repos(self):
        collab_repos = self.manager.list_collaborator_repos()

        repo_obj_list = []
        for repo in collab_repos:
            relative_uri = reverse('api:repo', args=(
                repo.repo_base, repo.repo_name))
            absolute_uri = self.base_uri + relative_uri

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'href': absolute_uri,
                'owner': repo.repo_base,
                })

        return {'repos': repo_obj_list}


class CollaboratorSerializer(DataHubSerializer):
    def list_collaborators(self, repo_name):
        collaborators = self.manager.list_collaborators(repo_name)

        collab_list = []
        for obj in collaborators:
            relative_uri = reverse('api:collaborator', args=(
                self.repo_base, repo_name, obj['username']))
            absolute_uri = self.base_uri + relative_uri

            collab_obj = {'username': obj['username'],
                          'href': absolute_uri}
            collab_list.append(collab_obj)

        return {'collaborators': collab_list}

    def describe_collaborator(self, repo, collaborator_username):
        collaborators = self.manager.list_collaborators(repo)
        for collaborator in collaborators:
            if collaborator['username'] == collaborator_username:
                return collaborator
        return collaborators

    def add_collaborator(self, repo, collaborator, db_permissions,
                         file_permissions):
        success = self.manager.add_collaborator(
            repo, collaborator, db_permissions, file_permissions)

        return success

    def remove_collaborator(self, repo, collaborator):
        success = self.manager.delete_collaborator(
            repo, collaborator)
        return success


class TableSerializer(DataHubSerializer):

    def create_table(self, repo, table, params):
        success = self.manager.create_table(repo, table, params)
        return success

    def list_tables(self, repo):
        tables = self.manager.list_tables(repo)
        table_list = []
        for table in tables:
            relative_uri = reverse('api:table', args=(
                self.repo_base, repo, table))
            absolute_uri = self.base_uri + relative_uri

            table_obj = {'table_name': table,
                         'href': absolute_uri}
            table_list.append(table_obj)

        return {'tables': table_list}

    def describe_table(self, repo, table, detail=False):
        res = self.manager.describe_table(
            repo=repo, table=table, detail=False)

        columns = []
        for column in res:
            response_obj = {}
            response_obj['column_name'] = column[0]
            response_obj['data_type'] = column[1]
            columns.append(response_obj)

        res = self.manager.list_table_permissions(repo, table)
        permissions = [permission for sublist in res for permission in sublist]

        return {'columns': columns, 'permissions': permissions}

    def delete_table(self, repo, table, force=False):
        success = self.manager.delete_table(repo, table, force)
        return success

    def export_table(self, repo, table, file_format='CSV', delimiter=',',
                     header=True):
        self.manager.export_table(
            repo=repo, table=table, file_format=file_format,
            delimiter=delimiter, header=header)


class ViewSerializer(DataHubSerializer):

    def create_view(self, repo, view, query):
        success = self.manager.create_view(repo, view, query)
        return success

    def list_views(self, repo):
        views = self.manager.list_views(repo)

        view_list = []
        for view in views:
            relative_uri = reverse('api:view', args=(
                self.repo_base, repo, view))
            absolute_uri = self.base_uri + relative_uri

            view_obj = {'view_name': view, 'href': absolute_uri}
            view_list.append(view_obj)

        return {'views': view_list}

    def describe_view(self, repo, view, detail=False):
        res = self.manager.describe_view(
            repo=repo, view=view, detail=False)

        response = []
        for column in res:
            response_obj = {}
            response_obj['column_name'] = column[0]
            response_obj['data_type'] = column[1]
            response.append(response_obj)
        return {'columns': response}

    def delete_view(self, repo, view, force=False):
        success = self.manager.delete_view(repo, view, force)
        return success

    def export_view(self, repo, view, file_format='CSV', delimiter=',',
                    header=True):
        self.manager.export_view(
            repo=repo, view=view, file_format=file_format,
            delimiter=delimiter, header=header)


class CardSerializer(DataHubSerializer):

    def list_cards(self, repo):
        cards = self.manager.list_repo_cards(repo)

        card_list = []
        for card in cards:
            relative_uri = reverse('api:card', args=(
                self.repo_base, repo, card))
            absolute_uri = self.base_uri + relative_uri

            card_obj = {'card_name': card, 'href': absolute_uri}
            card_list.append(card_obj)

        return {'cards': card_list}

    def describe_card(
            self, repo, card_name, current_page=1, rows_per_page=1000):
        card = self.manager.get_card(repo, card_name)
        # relative_uri = reverse('api:query_with_repo', args=(
        #     self.repo_base, repo))
        # absolute_uri = self.base_uri + relative_uri

        res = {}
        res['timestamp'] = card.timestamp
        res['query'] = card.query
        res['public'] = card.public

        # Get the results of the card
        # cards must spawn a new serializer, since they run as the user
        # that created the card (not necessarily the current user)
        query_serializer = QuerySerializer(self.repo_base, self.repo_base)
        query_results = query_serializer.execute_query(
            query=card.query, repo=repo, current_page=current_page,
            rows_per_page=rows_per_page,
            rows_only=None)
        res['results'] = query_results

        return res

    def update_card(self, repo, card_name, new_query, new_name, public):
        card = self.manager.update_card(
            repo, card_name, new_query, new_name, public)

        return self.describe_card(repo, card.card_name)

    def create_card(self, repo, card_name, query):
        card = self.manager.create_card(repo, card_name, query)

        return self.describe_card(repo, card.card_name)

    def delete_card(self, repo, card_name):
        return self.manager.delete_card(repo, card_name)

    def export_card(self, repo, card_name, file_format='CSV'):
        self.manager.export_card(repo, card_name, file_format)


class FileSerializer(DataHubSerializer):

    def list_files(self, repo):
        files = self.manager.list_repo_files(repo)
        file_list = []
        for file in files:
            relative_uri = reverse('api:file', args=(
                self.repo_base, repo, file))
            absolute_uri = self.base_uri + relative_uri

            file_obj = {'file_name': file, 'href': absolute_uri}
            file_list.append(file_obj)

        return {'files': file_list}

    def upload_file(self, repo, file):
        return self.manager.save_file(repo, file)

    def delete_file(self, repo, file_name):
        return self.manager.delete_file(repo, file_name)

    def get_file(self, repo, file_name):
        return self.manager.get_file(repo, file_name)


class QuerySerializer(DataHubSerializer):

    def execute_query(self, query, current_page=1,
                      rows_per_page=1000, repo=None,
                      rows_only=False):

        result = None
        result = self.manager.paginate_query(
            query, current_page, rows_per_page)

        rows = result.get('rows', None)
        columns = result.get('column_names', None)
        select_query = result.get('select_query', None)

        return_dict = {}
        return_dict['est_time_cost'] = result.get('time_cost', None)
        return_dict['est_byte_width'] = result.get('byte_width', None)
        return_dict['est_total_pages'] = result.get('total_pages', None)

        new_rows = []
        for row in rows:
            obj = {}
            for i in range(len(columns)):
                column = columns[i]
                obj[column] = row[i]
            new_rows.append(obj)

        return_dict['rows'] = new_rows

        # add appropriate link to previous and next:
        # next
        if rows_per_page <= len(rows):
            next_params = {
                "query": query,
                "current_page": current_page + 1,
                "rows_per_page": rows_per_page}
            return_dict['next_results_params'] = next_params

        if current_page > 1:
            previous_params = {
                "query": query,
                "current_page": current_page - 1,
                "rows_per_page": rows_per_page}
            return_dict['previous_results_params'] = previous_params

        if rows_only:
            # Some formats, like CSV, don't have a place for metadata.
            # Only return raw tabular data in those cases.
            if select_query:
                return return_dict['rows']
            else:
                return {}
        # By default, return the query result plus metadata.
        return return_dict


class RowLevelSecuritySerializer(object):

    def __init__(self, username):
        self.username = username

    def find_security_policies(
            self, repo=None, table=None, policy_id=None,
            policy=None, policy_type=None, grantee=None):

        res = RowLevelSecurityManager.find_security_policies(
            repo_base=self.username, repo=repo, table=table,
            policy_id=policy_id, policy=policy, policy_type=policy_type,
            grantee=grantee, grantor=self.username, safe=True)

        policies = [p._asdict() for p in res]

        return policies

    def create_security_policy(
            self, policy, policy_type, grantee, repo, table):

        res = RowLevelSecurityManager.create_security_policy(
            policy=policy,
            policy_type=policy_type,
            grantee=grantee,
            grantor=self.username,
            repo_base=self.username,
            repo=repo,
            table=table,
            safe=True)

        return res

    def update_security_policy(
            self, policy_id, new_policy, new_policy_type, new_grantee):

        res = RowLevelSecurityManager.update_security_policy(
            policy_id=policy_id,
            new_policy=new_policy,
            new_policy_type=new_policy_type,
            new_grantee=new_grantee,
            username=self.username)

        return res

    def remove_security_policy(self, policy_id):
        res = RowLevelSecurityManager.remove_security_policy(
            policy_id=policy_id,
            username=self.username)

        return res
