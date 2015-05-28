#!/usr/bin/python

from gen_py.datahub.account import AccountService
from gen_py.datahub import DataHub
from gen_py.datahub.constants import *
from gen_py.datahub.account.constants import *
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
  print "\n\nTrying to create and delete an account..."
  # This will initially thrown an exception since
  # You will need to register an application and assign
  # the variables below.
  # see the /developer/apps page to register an application.

  username="ACCOUNT_NAME"    
  password="ACCOUNT_PASSWORD"
  email="ACCOUNT_EMAIL"
  repo_name="REPO_NAME"       # the repository that your app operates on
  app_id="APP_ID"             # your app's unique id
  app_token="APP_TOKEN"       # your app's unique token

  datahub_transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
  datahub_transport = TTransport.TBufferedTransport(datahub_transport)
  datahub_protocol = TBinaryProtocol.TBinaryProtocol(datahub_transport)
  datahub_client = DataHub.Client(datahub_protocol)
  print "Version: %s" %(datahub_client.get_version())

  account_transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service/account')
  account_transport = TTransport.TBufferedTransport(account_transport)
  account_protocol = TBinaryProtocol.TBinaryProtocol(account_transport)
  account_client = AccountService.Client(account_protocol)


  # delete account
  try:
    print account_client.remove_account(
        username=username,
        app_id=app_id,
        app_token=app_token)
  except Exception, e:
    print e
    pass

  # create account
  try:
    print account_client.create_account(
        username=username,
        password=password,
        email=email,
        repo_name=repo_name,
        app_id=app_id,
        app_token=app_token)
  except Exception, e:
    print e


  print "\nTrying to query a user's table..."

  # RECOMMENDED (How an app should read/write in a users' repo)
  # Connect to the user repository through app_id + app_token.
  # Don't expose their password
  con_params_app = ConnectionParams(app_id=app_id, app_token=app_token, repo_base=username)
  con_app = datahub_client.open_connection(con_params=con_params_app)

  createSQL ="CREATE TABLE "+repo_name+".app_table(content text)"
  insertSQL = "INSERT INTO "+repo_name+".app_table VALUES('Anant Bhardwaj')"
  selectSQL = "SELECT * FROM "+repo_name+".app_table"

  print datahub_client.list_repos(con=con_app)
  print datahub_client.list_tables(con=con_app, repo_name=repo_name)
  print datahub_client.execute_sql(con_app, createSQL, query_params=None)
  print datahub_client.list_tables(con=con_app, repo_name=repo_name)
  print datahub_client.execute_sql(con_app, insertSQL, query_params=None);
  print datahub_client.execute_sql(con_app, selectSQL, query_params=None);

except Exception, e:
  print 'Something went wrong : %s' % (e)
