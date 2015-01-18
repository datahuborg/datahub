#!/usr/bin/python

from datahub.account import AccountService
from datahub import DataHub
from datahub.constants import *
from datahub.account.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample Python client for DataHub Account Creation
'''

try:
  datahub_transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
  datahub_transport = TTransport.TBufferedTransport(datahub_transport)
  datahub_protocol = TBinaryProtocol.TBinaryProtocol(datahub_transport)
  datahub_client = DataHub.Client(datahub_protocol)

  account_transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service/account')
  account_transport = TTransport.TBufferedTransport(account_transport)
  account_protocol = TBinaryProtocol.TBinaryProtocol(account_transport)
  account_client = AccountService.Client(account_protocol)

  
  print "Version: %s" %(datahub_client.get_version())


  
  # How an app can create a user account
  try:
    print account_client.create_account(username="confer",
                                password="confer",
                                email="confer@datahub.com",
                                repo_name="test",
                                app_id="confer",
                                app_token="d089b3ed-1d82-4eae-934a-859d7070d364")
  except Exception, e:
    print e


  
  
  # RECOMMENDED (How an app should read/write in a users' repo)
  # Connect to the user repository through app_id + app_token
  con_params_app = ConnectionParams(app_id='confer', app_token='d089b3ed-1d82-4eae-934a-859d7070d364', repo_base='confer_account')
  con_app = datahub_client.open_connection(con_params=con_params_app)
  print con_app
  print datahub_client.list_repos(con=con_app)
  print datahub_client.list_tables(con=con_app, repo_name='test')
  print datahub_client.execute_sql(con_app, "CREATE TABLE test.app_table(content text)", query_params=None)
  print datahub_client.list_tables(con=con_app, repo_name='test')
  print datahub_client.execute_sql(con_app, "INSERT INTO test.app_table VALUES('Anant Bhardwaj')", query_params=None);
  print datahub_client.execute_sql(con_app, "SELECT * FROM test.app_table", query_params=None);


  # NOT RECOMMENDED (never connect as an user through your app)
  # The following would work but DO NOT do it (connection w/ username + password)
  con_params_user = ConnectionParams(user='confer_account', password='confer')
  con_user = datahub_client.open_connection(con_params=con_params_user)
  print con_user
  print datahub_client.list_repos(con=con_user)
  print datahub_client.list_tables(con=con_app, repo_name='test')
  print datahub_client.execute_sql(con_user, "CREATE TABLE test.user_table(content text)", query_params=None)
  print datahub_client.list_tables(con=con_app, repo_name='test')
  print datahub_client.execute_sql(con_user, "INSERT INTO test.user_table VALUES('Anant Bhardwaj')", query_params=None);
  print datahub_client.execute_sql(con_user, "SELECT * FROM test.user_table", query_params=None);

  # FUN STUFF
  # App accessing a user-created table and User accessing an app-created table
  print datahub_client.execute_sql(con_user, "SELECT * FROM test.app_table", query_params=None);
  print datahub_client.execute_sql(con_app, "SELECT * FROM test.user_table", query_params=None);

except Exception, e:
  print 'Something went wrong : %s' % (e)
