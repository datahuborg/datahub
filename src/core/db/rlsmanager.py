
class RowLevelSecurityManager:

    def __init__(self, user, repo_base, repo, table):
        self.username = user
        self.repo_base = repo_base
        self.repo = repo
        self.table = table

    def list_security_policies(self):
        '''
        returns a list of all the security policies defined on the table
        '''
        pass

    def add_security_policy(self):
        '''
        creates a new security policy
        '''
        pass

    def update_security_policy(self):
        '''
        update an existing security policy
        '''
        pass

    def remove_security_policy(self):
        '''
        remove an existing security policy
        '''
        pass
