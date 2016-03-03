from config import settings
from core.db.connection import DataHubConnection
from django.contrib.auth.models import User
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


class RowLevelSecurityManager:

    def __init__(self, user, table, repo, repo_base):
        user = User.objects.get(username=user)
        self.username = user.username
        self.repo_base = repo_base
        self.repo = repo
        self.table = table

        self.user_con = DataHubConnection(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['USER'],
            repo_base='datahub')

    '''
    Policy Table Schema:
        id
        policy
        policy_type
        grantee
        grantor
        table_name
        repo
        repo_base
    '''

    def add_security_policy(self, policy, policy_type, grantee):
        '''
        creates a new security policy. check whether this policy exists in the
        table. If so, return an error, otherwise, create the policy in the
        policy table.
        '''
        return self.user_con.create_security_policy(policy, policy_type, grantee, self.username,
            self.table, self.repo, self.repo_base)
    
    def list_security_policies(self):
        '''
        returns a list of all the security policies defined on the table
        '''
        return self.user_con.list_security_policies(self.table, self.repo, self.repo_base)

    def find_security_policy(self, policy_id=None, policy=None, policy_type=None, grantee=None, grantor=None):
        '''
        Looks for security policies matching what the user specified. 
        '''
        return self.user_con.find_security_policy(self.table, self.repo, self.repo_base, policy_id, policy, policy_type, grantee, grantor)

    def find_security_policy_by_id(self, policy_id):
        '''
        Looks for a security policy matching the specified policy_id. 
        '''
        return self.user_con.find_security_policy_by_id(policy_id)

    def update_security_policy(self, policy_id, new_policy, new_policy_type, new_grantee):
        '''
        update an existing security policy
        '''
        return self.user_con.update_security_policy(policy_id, new_policy, new_policy_type, new_grantee, self.username)

    def remove_security_policy(self, policy_id):
        '''
        remove an existing security policy
        '''
        return self.user_con.remove_security_policy(policy_id)
   
