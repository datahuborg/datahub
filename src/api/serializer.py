from rest_framework import serializers
from django.contrib.auth.models import User

from inventory.models import Collaborator
from core.db.manager import DataHubManager


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_login', 'email')


class DataHubSerializer(object):

    def __init__(self, username, repo_base):
        self.username = username
        self.repo_base = repo_base
        self.manager = DataHubManager(
            user=self.username, repo_base=self.repo_base)


class RepoSerializer(DataHubSerializer):

    def create_repo(self, repo_name):
        success = False
        try:
            self.manager.create_repo(repo_name)
            success = True
        except:
            pass

        return(success)

    def delete_repo(self, repo_name, force=True):
        success = False
        try:
            self.manager.delete_repo(repo=repo_name, force=force)
            success = True
        except:
            pass

        return(success)

    def rename_repo(self, repo, new_name):
        success = False
        try:
            self.manager.rename_repo(repo=repo, new_name=new_name)
            success = True
        except:
            pass
        return(success)

    def user_owned_repos(self):
        repos = self.manager.list_repos()
        repos.sort()

        repo_obj_list = []
        for repo in repos:
            collaborators = self.manager.list_collaborators(repo)

            repo_obj_list.append({
                'repo_name': repo,
                'permissions': 'ALL',
                'collaborators': collaborators,
                'owner': self.username
                })

        return {'repos': repo_obj_list}

    def user_accessible_repos(self):
        user_owned_list = self.user_owned_repos()['repos']
        all_collab_list = self.all_collab_repos()['repos']
        return {'repos': user_owned_list + all_collab_list}

    def specific_collab_repos(self, collab_username):
        # get the collaborators
        user = User.objects.get(username=self.username)
        collab_repos = Collaborator.objects.filter(user=user)

        repo_obj_list = []
        for repo in collab_repos:
            collaborators = self.manager.list_collaborators(repo.repo_name)

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'permissions': repo.permission,
                'owner': repo.repo_base,
                'collaborators': collaborators
                })

        return {'repos': repo_obj_list}

    def all_collab_repos(self):
        collab_repos = self.manager.list_collaborator_repos()

        repo_obj_list = []
        for repo in collab_repos:
            collaborators = self.manager.list_collaborators(repo.repo_name)

            repo_obj_list.append({
                'repo_name': repo.repo_name,
                'privileges': repo.permission,
                'owner': repo.repo_base,
                'collaborators': collaborators
                })

        return {'repos': repo_obj_list}


class CollaboratorSerializer(DataHubSerializer):
    def list_collaborators(self, repo_name):

        collaborators = self.manager.list_collaborators(repo_name)
        return collaborators

    def add_collaborator(self, repo, collaborator, privileges):
        success = False
        try:
            self.manager.add_collaborator(
                repo, collaborator, privileges)
            success = True
        except:
            pass

        return success

    def remove_collaborator(self, repo, collaborator):
        success = False
        try:
            self.manager.delete_collaborator(
                repo, collaborator)
            success = True
        except:
            pass
        return success


class TableSerializer(DataHubSerializer):

    def create_table(self, repo, table, params):
        success = False
        try:
            self.manager.create_table(repo, table, params)
            success = True
        except:
            pass

        return success

    def list_tables(self, repo):
        tables = self.manager.list_tables(repo)
        return tables

    def describe_table(self, repo, table, detail=False):
        try:
            res = self.manager.describe_table(
                repo=repo, table=table, detail=False)

            response = []
            for column in res:
                response_obj = {}
                response_obj['column_name'] = column[0]
                response_obj['data_type'] = column[1]
                response.append(response_obj)
            return response

        except:
            return False


class QuerySerializer(DataHubSerializer):

    def execute_sql(self, query, repo=None):

        if repo:
            self.manager.set_search_paths([repo])
            # search_path = 'set search_path to %s; ' % (repo)
            # query = search_path + query

        success = False
        try:
            result = self.manager.execute_sql(query)
            success = True
        except:
            # this should really return the error message, but I haven't
            # worked that out yet.
            result = {}
            pass

        # rename the tuples key to rows
        result['rows'] = result.pop('tuples', None)
        result['columns'] = result.pop('fields', None)

        return (success, result)
