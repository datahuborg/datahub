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

  try:
    print account_client.remove_account(username="confer_account",
                                app_id="confer",
                                app_token="d089b3ed-1d82-4eae-934a-859d7070d364")
  except:
    pass

  
  print account_client.create_account(username="confer_account",
                              password="confer",
                              email="confer@datahub.com",
                              repo_name="test",
                              app_id="confer",
                              app_token="d089b3ed-1d82-4eae-934a-859d7070d364")

  # open connection
  con_params = ConnectionParams(app_id='confer', app_token='d089b3ed-1d82-4eae-934a-859d7070d364', repo_base='confer_account')
  con = datahub_client.open_connection(con_params=con_params)
  print con
  print datahub_client.list_repos(con=con)
  print datahub_client.execute_sql(con, "CREATE TABLE test.data(content text)", query_params=None)
  print datahub_client.execute_sql(con, "INSERT INTO test.data VALUES('Anant Bhardwaj')", query_params=None);
  print datahub_client.execute_sql(con, "SELECT * FROM test.data", query_params=None);


  print account_client.remove_account(username="confer_account",
                              app_id="confer",
                              app_token="d089b3ed-1d82-4eae-934a-859d7070d364")

except Exception, e:
  print 'Something went wrong : %s' % (e)
