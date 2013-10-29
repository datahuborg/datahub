import sys, logging, time, base64, datetime
from schema.models import *


'''
Datahub Main Controller

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

def list_databases(username):
	res = {'status':False}
	try:
		user = User.objects.get(username=username)
		databases = Database.objects.filter(owner = user)
		db_names =[database.db_name for database in databases]
		res['status'] = True
		res['db_names'] = db_names			
	except:
		print sys.exc_info()[0]
		res['code'] = 'UNKNOWN_ERROR'
	logging.debug(res)
	return res



def list_tables(db_name):
	res = {'status':False}
	try:
		con = Connection(db_name = db_name)
		res = con.list_tables()
		res['table_names'] = res['data']			
	except:
		print "list_tables"
		print sys.exc_info()[0]
		res['code'] = 'UNKNOWN_ERROR'
	logging.debug(res)
	return res
	


def create_database(username, db_name):
	res = {'status':False}
	try:
		user = User.objects.get(username=username)
		dbname = user.username + '_' + db_name
		con = Connection();
		con.create_database(dbname)
		db = Database(owner = user, db_name = dbname)		
		db.save()
		res['status'] = True				
	except:
		print "create_database"
		print sys.exc_info()[0]
		res['code'] = 'UNKNOWN_ERROR'
	logging.debug(res)
	return res



def create_table(db_name, table_name):
	res = {'status':False}
	try:
		db = Database.objects.get(db_name = db_name)
		con = Connection(db_name = db_name);
		con.create_table(table_name)
		res['status'] = True				
	except:
		print "create_table"
		print sys.exc_info()[0]
		res['code'] = 'UNKNOWN_ERROR'
	logging.debug(res)
	return res


	
