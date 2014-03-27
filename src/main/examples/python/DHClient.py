#!/usr/bin/python

from datahub import DataHub
from datahub.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code accesing DataHub APIs
'''



try:

  transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DataHub.Client(protocol)
  print client.get_version()
  
  con_params = DHConnectionParams(user='anantb', password='anant')
  con = client.connect(con_params=con_params)

  res  = client.execute_sql(
      con=con,
      query='select * from anantb.demo.team',
      query_params=None)

  print res

except Exception, e:
    print 'Something went wrong : %s' % (e)
