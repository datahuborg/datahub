from core.db.rlsmanager import RowLevelSecurityManager
import re


class RLSPermissionsParser:

    def __init__(self, repo_base, user):
        self.repo_base = repo_base
        self.user = user

    def process_permissions(self, permission):
        '''
        Takes in the SQL permissions statement, extracts all the necessary
        components (permission type, grantee, repo_name, table_name, and
        permission) and creates a security policy for it in the policy table.
        '''
        permission_type = self.extract_permission_type(permission)
        access_type = self.extract_access_type(permission)
        grantee = self.extract_grantee(permission)
        extract_table_info = self.extract_table_info(permission)
        policy = self.extract_policy(permission)

        repo = extract_table_info[0]
        table = extract_table_info[1]

        if permission_type == "grant":
            RowLevelSecurityManager.create_security_policy(
                policy=policy,
                policy_type=access_type,
                grantee=grantee,
                grantor=self.user,
                repo_base=self.repo_base,
                repo=repo,
                table=table)
        else:
            # Need to remove policy if it is remove
            policies = RowLevelSecurityManager.find_security_policies(
                repo_base=self.repo_base,
                repo=repo,
                table=table,
                policy=policy,
                policy_type=access_type,
                grantee=grantee,
                grantor=self.user,
                safe=False)

            if len(policies) == 1:
                RowLevelSecurityManager.remove_security_policy(
                    policy_id=policy[0][0], username=self.user,
                    repo_base=self.repo_base)
            else:
                raise Exception('Error identifying security policy.')

    def extract_permission_type(self, permission):
        '''
        Takes in a SQL permissions statement, extracts the permission type,
        and returns it in the form of a string. There are two types of
        permissions: Grant and Revoke. Throws an exception if the
        permissions statement does not contain a matching type.
        '''
        valid_permission_types = ["grant", "revoke"]
        try:
            result = permission.split(' ', 1)[0].lower()
        except:
            raise Exception('Failed to parse permission type from '
                            'permission query.')
        if result not in valid_permission_types:
            raise Exception('%s is not a valid permission type.' % result)

        return result

    def extract_access_type(self, permission):
        '''
        Takes in a SQL permissions statement, extracts the access type,
        and returns it in the form of a string. Throws an exception
        if the permissions statement does not contain an access type or
        is an invalid one.
        '''
        valid_access_types = ["select", "insert", "update"]

        try:
            if permission.split(' ', 1)[0].lower() == "grant":
                result = re.search("grant (.*) access", permission)
                result = result.group(1).lower()
            else:
                result = re.search("revoke (.*) access", permission)
                result = result.group(1).lower()
        except:
            raise Exception('Failed to create security policy due to '
                            'incorrect syntax.')

        if result not in valid_access_types:
            raise Exception('Failed to create security policy. '
                            '%s is not a valid access type.' % result)
        return result

    def extract_grantee(self, permission):
        '''
        Takes in a SQL permissions statement, extracts the grantee, and returns
        it in the form of a string. Throws an exception if the permissions
        statement does not contain a grantee.
        '''
        try:
            result = re.search("to (.*) on", permission)
            return result.group(1)
        except:
            raise Exception('Failed to create security policy due to '
                            'incorrect syntax.')

    def extract_table_info(self, permission):
        '''
        Takes in a SQL permissions statement, extracts the table information,
        and returns it in the form of a list of [repo_base, table_name]. Throws
        an exception if the permissions statement does not contain information
        about the table or if it is in the wrong format.
        '''
        try:
            result = re.search("on (.*) where", permission)
            table_info = result.group(1).split(".")
            return table_info
        except:
            raise Exception('Failed to create security policy due to '
                            'incorrect syntax.')

    def extract_policy(self, permission):
        '''
        Takes in a SQL permissions statement, extracts the policy information,
        and returns it in the form of a string. Throws an exception if the
        permissions statement does not define any security policies.
        '''
        try:
            result = re.search("where (.*)", permission)
            return result.group(1)
        except:
            raise Exception('Failed to create security policy due to '
                            'incorrect syntax.')
