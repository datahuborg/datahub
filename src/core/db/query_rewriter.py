import sqlparse
import re
from core.db.rlsmanager import RowLevelSecurityManager

class SQLQueryRewriter:


    def __init__(self, repo_base, user):
        self.repo_base = repo_base
        self.user = user


    def contain_subquery(self, token):
        '''
        Takes in a sqlparse token and checks whether it contains a subquery
        '''
        if not token.is_group():
            return False
        if "select" not in token.to_unicode().lower():
            return False
        return True


    def apply_row_level_security(self, query):
        '''
        Takes in a SQL query and applies row level security to it. First, all the subqueries are adjusted to include
        security policies. Afterwards, all the join query components will have table names replaced by RLS subqueries.
        '''
        subquery_with_rls = self.process_subqueries(query)
        result = self.process_join_query(subquery_with_rls).rstrip()
        if result[-1] != ";":
            result += ";"
        return result


    def process_subquery(self, token):
        '''
        Takes in 
        a subquery token and turns it into a SQL string with row level security applied to the subquery.
        '''
        result = ''
        parsed_subquery = self.extract_subquery(token)
        result += parsed_subquery[0]
        result += self.process_subqueries(parsed_subquery[1])
        result += parsed_subquery[2].replace(";", "")
        return result


    def found_join(self, join_found, token):
        '''
        Checks whether the token is a join token (this is diffrent from a subquery that contains a join).
        '''
        joins = ["join", "left join", "right join", "full join", "inner join"]
        if token.to_unicode().lower() in joins:
            return True
        return join_found



    def extract_table_information(self, table, token):
        '''
        Pulls out the table information from the token if it exists, or returns the original table information.
        '''
        try:
            if token.get_name() != None and token.get_parent_name() != None:
                return (token.get_parent_name(), token.get_name())
        except Exception:
            return table
        return table
 

    def need_apply_row_level_security(self, join_present, table_information, token=None, row_level_security_applied=None):
        '''
        Checks whether row level security need to be applied.
        '''
        if join_present or table_information is None:
            return False
        if token is not None and "where" in token.value.lower():
            return True
        if row_level_security_applied is not None and not row_level_security_applied:
            return True
        return False


    def get_security_policy_string(self, table_information, where_found=False):
        '''
        Extracts out all security policies related to the table information specified, and turns the policies into
        a singular SQL string to append to the original query. 
        '''
        result = ''
        policies = self.find_security_policy(table_information[0], table_information[1], "ALL")
        if policies is None:
            return result
        if where_found:
            result += " AND "
        else:
            result += " WHERE "
        for policy in policies:
            result += policy + " AND "
        return result[:-5]


    def contains_join_subquery(self, token):
        '''
        Checks if the token contains a subquery. If the word "join" is in the token, but it is not the only word,
        then this must be a join subquery
        '''
        if not self.contains_join(token) and "join" in token.to_unicode().lower():
            return True
        return False


    def process_subqueries(self, query):
        '''
        Method for processing a query filled with subqueries. Will apply row level security to all the subqueries to append
        security policies to the queries. 
        '''
        tokens = sqlparse.parse(query)[0].tokens
        result = ''

        table_information = None
        rls_applied = False
        join_present = False

        for token in tokens:
            if self.contain_subquery(token):
                result += self.process_subquery(token)
            else:
                result += token.to_unicode()

            table_information = self.extract_table_information(table_information, token)
            join_present = self.found_join(join_present, token)

            if self.need_apply_row_level_security(join_present, table_information, token=token):
                result += self.get_security_policy_string(table_information, True)
                rls_applied = True

        if self.need_apply_row_level_security(join_present, table_information, row_level_security_applied=rls_applied):
            result += self.get_security_policy_string(table_information, False)
        return result



    def process_join_subquery(self, token):
        '''
        Method for processing subqueries with joins. Turning tokens with a join subquery into 
        a singular query string.
        '''
        result = ''
        parsed_subquery = self.extract_subquery(token)
        result += parsed_subquery[0]
        result += self.process_join_query(parsed_subquery[1])
        result += parsed_subquery[2].replace(";", "")
        return result



    def convert_join_token_to_query(self, token):
        result = ''
        #check if token is a subquery or a table. Transform it if it is a table
        if self.extract_repo_table_from_token(token):
            # If the token is simply a table name, then apply RLS
            result += '%s ' % self.transform_table_to_rls_subquery(token)
        else:
            # Otherwise, token is already a subquery, so append it to the original query
            result += '%s ' % token.to_unicode()
        return result
   
    

    def process_join_query(self, query):
        '''
        Method for processing queries filled with joins. Converts all table names before and after joins into 
        a subquery with row level security applied.
        '''
        tokens = sqlparse.parse(query)[0].tokens

        prev_token = None
        join_found = False
        final_query = ''
        
        for token in tokens:
            if self.contains_join_subquery(token):
                final_query += '%s ' % prev_token.to_unicode()
                final_query += self.process_join_subquery(token)
                prev_token = None
                continue

            # The previous token was a join, need to check if current token is a subquery or a table. Transform it if it is a table
            if join_found:
                if token.value == " ":
                     final_query += token.to_unicode()
                else:
                    final_query += self.convert_join_token_to_query(token)
                    prev_token = None
                    join_found = False
                continue
 
            # If current token is a join, then need to convert prev_token to subquery and append that first
            if self.contains_join(token):
                final_query += self.convert_join_token_to_query(prev_token)
                final_query += '%s ' % token.to_unicode()
                join_found = True

            # If current token is not a join, add previous token if it is not none, and set previous toekn to current token
            elif token.to_unicode() != " ":
                if prev_token != None:
                    final_query += '%s ' % prev_token.to_unicode()
                prev_token = token
            

        # Need to process the last token (it was skipped in the previous loop because it's the last one)
        if join_found:
            if prev_token.value == " ":
                final_query += prev_token.to_unicode();
            else:
                final_query += self.convert_join_token_to_query(prev_token)
        else:
            if prev_token != None and prev_token.value != ";":
                final_query += '%s ' % prev_token.to_unicode()

        return final_query



    def transform_table_to_rls_subquery(self, token):
        '''
        Takes in information about a table and turns it into a subquery with row level security applied.
        '''
        table_information = self.extract_repo_table_from_token(token)
        security_policies = self.find_security_policy(table_information[0], table_information[1], "ALL")
        query_result = "(SELECT * FROM %s.%s" % (table_information[0], table_information[1])
        if security_policies:
            query_result += (" WHERE %s" %  security_policies[0])
            for policy in security_policies[1:]:
                query_result += (" AND %s" % policy)
        query_result += ")"
        return query_result

    
    def contains_join(self, token):
        '''
        Checks whether the token is a join token.
        '''
        joins = ["join", "left join", "right join", "full join", "inner join"]
        if token.to_unicode().lower() in joins:
            return True
        return False

    

    def extract_subquery(self, token):
        '''
        Takes in a sqlparse token that contains a subquery and returns the subquery as a SQL stirng. Subquery will be nested in between
        parentheses, so just return the phrase in between. 
        '''
        subquery_start_index = token.to_unicode().find('(')
        subquery_end_index = token.to_unicode().rfind(')')
        return (token.to_unicode()[:subquery_start_index+1], token.to_unicode()[subquery_start_index+1:subquery_end_index], token.to_unicode()[subquery_end_index:])  
 


    def find_security_policy(self, table, repo, policytype):
        '''
        Looks up policies associated with the table and repo and returns a list of all the policies defined.
        Dummy method right now, need to create the policies table and insert all of this inside. 
        '''
        row_level_security_manager = RowLevelSecurityManager(
            user=self.user,
            table=table,
            repo=repo, 
            repo_base=self.repo_base)
        security_policies = row_level_security_manager.find_security_policy(policy_type=policytype, grantee=self.user)
        print security_policies
        #return security_policies

        #return [('a=b')]
        return []


    def extract_repo_table_from_token(self, token):
        '''
        Takes in a token and extracts out the table information from the token (repo, tablename) if it exists, otherwise return None
        '''
        try:
            if token.get_name() != None and token.get_parent_name() != None:
                return (token.get_parent_name(), token.get_name())
        except Exception:
            return None
        return None
 