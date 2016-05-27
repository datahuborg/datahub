import sqlparse

from inventory.models import Collaborator
from core.db.rlsmanager import RowLevelSecurityManager
from config import settings


class SQLQueryRewriter:

    def __init__(self, repo_base, user):
        self.repo_base = repo_base
        self.user = user

    def extract_table_info(self, table_string):
        '''
        Takes in a string and parses it for the repo and table name.
        Tables are typically in the form of repo_name.table_name, so
        in this function, we check if the string is of the right form. If so,
        we return a list of [repo_name, table_name, repo_base].
        Otherwise, we return None.

        Valid table infos can be of form repo.table or repo_base.repo.table
        '''
        table_info = table_string.rstrip().split('.')
        if len(table_info) == 2:
            return [table_info[0], table_info[1], None]
        if len(table_info) == 3:
            return [table_info[1], table_info[2], table_info[0]]

        raise Exception('Error parsing %s: missing schema name' % table_string)

    def extract_table_string(self, table):
        '''
        Takes in a string and parses it for the table information. First,
        we take the table input and splits it by spaces to separate the table
        information from aliasing information. For example, if the table is of
        the form:

            (1) repo_name.table_name
            (2) repo_name.table_name AS alias_name
            (3) repo_name.table.name alias_name

        this function will return:

            (1) ([repo_name,table_name], '')
            (2) ([repo_name,table_name], 'AS alias_name')
            (3) ([repo_name,table_name], 'alias_name')

        If the table input is of the wrong form where the first phrase does
        not contain table information, then this function will return None.
        '''
        table_input = table.rstrip().split(' ')
        if table_input[0] != '':
            table_info = self.extract_table_info(table_input[0])
            if table_info is None:
                return None
            alias_info = " ".join(table_input[1:])
            return (table_info, alias_info)
        return None

    def extract_table_token(self, token):
        '''
        Takes in a token and returns a list of table information for each of
        the tables in the token. There may be multiple tables in the token
        because SQLParse parses all text after the FROM token and before the
        next SQL key word in the query as the table name. For example, if
        we have a query like:

            "SELECT * from repo1.table1 as tbl1, repo2.table2 as tbl2 where..."

        then "repo1.table1 as tbl1, repo2.table2 as tbl2" will fall into one
        token. This method will return a list of table information for all
        tables in a token.
        '''
        table_list = []
        token_string = token.to_unicode()
        tables = token_string.split(',')
        for table in tables:
            table_info = self.extract_table_string(table.rstrip().lstrip())
            if table_info is not None:
                table_list.append((table_info[0], table_info[1]))
        return table_list

    def contains_subquery(self, token):
        '''
        Takes in a token and checks whether the token contains a subquery
        inside it. Return True if so, False otherwise.
        '''
        if not token.is_group():
            return False
        if "select" not in token.to_unicode().lower():
            return False
        return True

    def extract_subquery(self, token):
        '''
        Takes in a token that contains a subquery and returns a tuple of the
        form (string_before_subquery, subquery_string, string_after_subqery).
        All subqueries are nested in between parantheses, so we are just
        separating the subquery from the other parts that come before and
        after the query.
        '''
        subquery_start = token.to_unicode().find('(')
        subquery_end = token.to_unicode().rfind(')')
        return (token.to_unicode()[:subquery_start + 1],
                token.to_unicode()[subquery_start + 1:subquery_end],
                token.to_unicode()[subquery_end:])

    def process_subquery(self, token):
        '''
        Takes in a token and processes the subquery that it contains. First,
        we call extract_subquery to extract the subquery from the
        string that comes before and after it. Then, we apply row level
        security to the extracted subquery, and merge the result with the other
        string components.
        '''
        result = ''
        subquery = self.extract_subquery(token)
        result = subquery[0] + '%s' + subquery[2]
        processed_subquery = self.apply_row_level_security(
            subquery[1].rstrip().lstrip())
        return result % processed_subquery

    def apply_row_level_security(self, query):
        token = sqlparse.parse(query)[0].tokens[0].to_unicode().lower()
        if token == "insert":
            return self.apply_row_level_security_insert(query)
        elif token == "update":
            return self.apply_row_level_security_update(query)
        elif token == "explain" or token == "select":
            return self.apply_row_level_security_base(query)
        return query

    def apply_row_level_security_insert(self, query):
        '''
        Takes in an insert SQL query and applies security policies related to
        the insert access type to it. Currently, we only support one type
        of insert permission -- which is that the user making the insert call
        has permission to insert into the specified table.

        # Insert into repo.table values (...)
        # Insert into repo.table values (select * from ....)
        '''
        # Find the table of interest, and check if any meta user insert
        # policies are defined on the table (user='username'). If so,
        # return the query as entered, as the user has insert permissions. If
        # not, raise an exception stating user does not have insert
        # permissions.

        tokens = sqlparse.parse(query)[0].tokens
        prev_token = None
        result = ''

        table = None
        for token in tokens:
            if self.contains_subquery(token):
                result += self.process_subquery(token)
                prev_token = token
                continue

            if (prev_token is None or token.to_unicode() == " " or
                    prev_token.to_unicode().lower() != "into"):
                result += token.to_unicode()
                if token.to_unicode() != " ":
                    prev_token = token
                continue

            table = self.extract_table_string(token.to_unicode())
            result += token.to_unicode()
            if token.to_unicode() != " ":
                prev_token = token

        if table is not None:
            policy = self.find_table_policies(
                table[0][1], table[0][0], "insert", table[0][2])

            if policy == [] or policy[0] == "INSERT='True'":
                return result

        raise Exception('User does not have insert access on %s' % table[0][1])

    def apply_row_level_security_update(self, query):
        '''
        Takes in an update SQL query and applies security policies related to
        the update access type to it.
        '''
        tokens = sqlparse.parse(query.replace(";", ''))[0].tokens
        prev_token = None
        result = ''

        table = None
        for token in tokens:
            if self.contains_subquery(token):
                result += self.process_subquery(token)
                continue

            if (prev_token is None or token.to_unicode() == " " or
                    prev_token.to_unicode().lower() != "update"):
                result += token.to_unicode()
                if token.to_unicode() != " ":
                    prev_token = token
                continue

            table = self.extract_table_info(token.to_unicode())
            result += token.to_unicode()
            if token.to_unicode() != " ":
                prev_token = token

        if table is not None:
            policies = self.find_table_policies(
                table[1], table[0], "update", table[2])
            for policy in policies:
                result += (' AND %s' % policy)

        result = result.replace("USERNAME", "'" + self.user + "'")
        return result

    def is_postgres_catalog(self, token):
        token_name = token.to_unicode()
        if token_name[:3] == 'pg_':
            return True
        return False

    def need_query_rewrite(self, prev_token):
        prev_token = prev_token.to_unicode().lower()
        joins = ["inner join", "left join", "right join", "join"]
        if prev_token == "from" or prev_token in joins:
            return True
        return False

    def apply_row_level_security_base(self, query):
        '''
        Takes in a SQL query and applies row level security to it. All table
        references in the query are replaced with a subquery that only extracts
        rows from the table for which the user is allowed to see.
        '''
        tokens = sqlparse.parse(query)[0].tokens
        replace_list = []
        prev_token = None
        result = ''

        for token in tokens:
            if self.contains_subquery(token):
                result += self.process_subquery(token)
                prev_token = token
                continue

            if self.is_postgres_catalog(token):
                result += token.to_unicode()
                prev_token = token
                continue

            if (prev_token is None or token.to_unicode() == " " or
                    not self.need_query_rewrite(prev_token)):
                result += token.to_unicode()
                if token.to_unicode() != " ":
                    prev_token = token
                continue

            table_information = self.extract_table_token(token)
            for table in table_information:
                if table[0][2] is not None:
                    query = '(SELECT * FROM %s.%s.%s' % (
                        table[0][2], table[0][0], table[0][1])
                else:
                    query = '(SELECT * FROM %s.%s' % (table[0][0], table[0][1])

                policies = self.find_table_policies(table[0][1],
                                                    table[0][0],
                                                    "select",
                                                    table[0][2])
                if policies:
                    query += ' WHERE '
                    for policy in policies:
                        query += policy + " OR "
                    query = query[:-4]
                query += ")"

                # Here we are handling table aliasing. In the case where the
                # default query does not use an alias, we need to auto-create
                # an alias for the table (since we are constructing a subquery
                # from the table name to apply row level security). We then
                # need to replace all later instances of the original table
                # with the alias.
                if table[1] != "":
                    query += " %s" % table[1]
                else:
                    original_table_name = table[0][0] + "." + table[0][1]
                    alias_name = table[0][0] + table[0][1]
                    query += " AS %s" % (alias_name)
                    replace_list.append((original_table_name,
                                         alias_name,
                                         len(result) + len(query)))

                result += query
                if len(table_information) > 1:
                    result += ", "

            if len(table_information) > 1:
                result = result[:-2]

            prev_token = token

        for alias in replace_list:
            result = result[0:alias[2]] + result[alias[2]:].replace(
                alias[0] + ".", alias[1] + ".")
            result = result[0:alias[2]] + result[alias[2]:].replace(
                alias[0] + " ", alias[1] + " ")

        result = result.replace("USERNAME", "'" + self.user + "'")
        return result

    def find_table_policies(self, table, repo, policytype, repo_base):
        '''
        Look up policies associated with the table and repo and returns a
        list of all the policies defined for the user.
        '''

        if repo_base is None:
            repo_base = self.repo_base

        # policies that are meant to apply to specific users
        user_policies = RowLevelSecurityManager.find_security_policies(
            repo_base=repo_base,
            repo=repo,
            table=table,
            policy_type=policytype,
            grantee=self.user,
            safe=False)

        # policies that are meant to apply to all users
        all_policies = RowLevelSecurityManager.find_security_policies(
            repo_base=repo_base,
            repo=repo,
            table=table,
            policy_type=policytype,
            grantee=settings.RLS_ALL,
            safe=False)

        # People collaborating on this repo
        collaborators = Collaborator.objects.filter(repo_base=repo_base,
                                                    repo_name=repo)

        # If the user is not explicitly granted access, also load the
        # public_policies
        public_policies = []
        if self.user not in collaborators:
            public_policies = RowLevelSecurityManager.find_security_policies(
                repo_base=repo_base,
                repo=repo,
                table=table,
                policy_type=policytype,
                grantee=settings.RLS_PUBLIC,
                safe=False)

        security_policies = user_policies + all_policies + public_policies

        result = []
        for policy_tuple in security_policies:
            result.append(policy_tuple.policy)

        return result
