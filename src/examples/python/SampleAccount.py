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

  print account_client.remove_account(username="confer_account",
                              app_id="confer",
                              app_token="57f2acbc-5776-4aa3-9068-0b8f8321ff78")

  print account_client.create_account(username="confer_account",
                              password="confer",
                              email="confer@datahub.com",
                              repo_name="test",
                              app_id="confer",
                              app_token="57f2acbc-5776-4aa3-9068-0b8f8321ff78")

  # open connection
  con_params = ConnectionParams(user='confer', password='57f2acbc-5776-4aa3-9068-0b8f8321ff78', repo_base='confer_account')
  con = datahub_client.open_connection(con_params=con_params)
  print con.execute_sql("CRETAE TABLE test.data(content text)")
  print con.execute_sql("INSERT INTO test.data VALUES('Anant Bhardwaj')");
  print con.execute_sql("SELECT * FROM test.data");


  print account_client.remove_account(username="confer_account",
                              app_id="confer",
                              app_token="57f2acbc-5776-4aa3-9068-0b8f8321ff78")

except Exception, e:
  print 'Something went wrong : %s' % (e)
