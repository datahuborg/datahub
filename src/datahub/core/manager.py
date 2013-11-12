from core.db.connection import *
from schema.models import *


'''
Datahub Account Manager

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

def create_user(username, password):
	res = Connection.create_user(
			username=username, password=password)
	return res


def list_databases(username):
	res = Connection.list_databases(username=username)
	return res

def list_repos(username):
  res = Connection.list_databases(username=username)
  return res

def list_tables(username, db_name):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password,
      db_name=db_name)
  res = con.list_tables()
  return res

def load_table(username, db_name, table_name):
  user = User.objects.get(username=username)
  con = Connection(
      user=username,
      password=user.password,
      db_name=db_name)
  res = con.execute_sql('SELECT * FROM %s' %(table_name))
  return res