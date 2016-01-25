from rest_framework import serializers
from django.contrib.auth.models import User

from core.db.manager import DataHubManager


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'last_login', 'first_name', 'last_name', 'email')


class DataHubSerializer(serializers.BaseSerializer):
    # def __init__(self, username, repo_base=None, many=False):
    #     serializers.BaseSerializer.__init__(self)

        # self.username = username
        # self.user = User.objects.get(username=self.username)
        # if not repo_base:
        #     self.repo_base = username

    def to_representation(self, obj):
        # import pdb; pdb.set_trace()

        username = obj
        repo_base = username

        manager = DataHubManager(user=username, repo_base=repo_base)
        repos = manager.list_repos()
        return {'repos': repos}





# class UserRepoSerializer(DataHubSerializer):
#     def __init__(self, username, repo_base=None):
#         self = DataHubSerializer.__init__(self, username=username, repo_base=repo_base)
#         import pdb; pdb.set_trace()
#         print(self)


#     import pdb; pdb.set_trace()
#     # data = self.manager.list_repos()
#     data = 'foo'
