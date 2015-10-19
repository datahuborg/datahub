import hashlib
import sqlparse


from account.manager import *
from core.db.connection import DataHubConnection
from core.db.manager import DataHubManager

from datahub import DataHub
from datahub.constants import *
from datahub.account.constants import *

'''
@author: Kelly Zhang
@date: March 11, 2015

RowLevelSecurity Handler
'''

class RowLevelSecurityHandler:
  def __init__(self):
	self.sessions={}
	pass

  def create_security_policy(self, user_name, policy):
	pass

  def update_security_policy(self, user_name, policy):
	pass

  def view_security_policy(self, user_name, table_name, command_name):
	pass

  def remove_recurity_policy(self, user_name, policy):
	pass

  def view_policy_set(self, user_name):
	pass

  def filter_sql_query(self, username, sql_query):
	result = sqlparse.parse(sql_query)
	stmt = result[0]
	tokens = stmt.tokens

	### First need to look up the repo and table name
	repo = None
	table = None
	for token in tokens:
		try:
			if token.get_parent_name() != None and token.get_name() != None:
				repo  = token.get_parent_name()
				table = token.get_name()
		except Exception:
			pass

	### Second need to look up the type of SQL Query Access This is
	query_type = tokens[0].to_unicode()


	### Third need to look up predicates with repo information
	accessPolicies = TablePolicy.objects.filter(repo_name=repo, table_name=table, policy_type=query_type)

	if not accessPolicies:
		# If nothing defined for accessPolicies, check if something is defined for All
		accessPolicies = TablePolicy.objects.filter(repo_name=repo, table_name=table, policy_type="All")

	predicateInfo = None
	if accessPolicies:
		for policy in accessPolicies:
			pred = policy.predicates
			if "username" in policy.predicates:
				pred = policy.predicates.replace("username", "'" + username + "'")
			if not predicateInfo:
				predicateInfo = pred
			else:
				predicateInfo = predicateInfo + " and " + pred

	### Finally, need to reconstruct the SQL Statement to incorporate these predicates
	query = ""
	where_found = False
	for token in tokens:
		str_tkn = token.to_unicode()
		query = query + str_tkn
		if "where" in token.value and predicateInfo:
			query = query + " and " + predicateInfo
			where_found = True

	if not where_found and predicateInfo:
		query = query + " where " + predicateInfo


	return query