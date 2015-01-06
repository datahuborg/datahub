#!/usr/bin/python

from datahub.account import AccountService
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
  transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service/account')
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = AccountService.Client(protocol)

  
  print "Version: %s" %(client.get_version())

  print client.create_account(username="test_account",
                              password="test",
                              email="test@test.com",
                              app_id="test",
                              app_token="f61c8d32-54a8-4978-afc8-c45f9f73a55e")

  print client.remove_account(username="test_account",
                              app_id="test",
                              app_token="f61c8d32-54a8-4978-afc8-c45f9f73a55e")

except Exception, e:
    print 'Something went wrong : %s' % (e)
