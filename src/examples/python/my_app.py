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

Sample Python client for DataHub
'''

try:
  transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DataHub.Client(protocol)
  
  print "Version: %s" %(client.get_version())
  
  # open connection
  con_params = ConnectionParams(user='anantb', password='anant')
  con = client.open_connection(con_params=con_params)

  # execute a query
  res  = client.execute_sql(
      con=con,
      query='create table if not exists pawademo.teams (names text)',
      query_params=None)

  res  = client.execute_sql(
      con=con,
      query="insert into pawademo.teams  values('Telecommunication')",
      query_params=None)

  res  = client.execute_sql(
      con=con,
      query="insert into pawademo.teams  values('Analytics')",
      query_params=None)

  res  = client.execute_sql(
      con=con,
      query='select * from anantb.pawademo.teams',
      query_params=None)

  # print field names
  print "\t".join(res.field_names)
  
  # print tuples
  for t in res.tuples:
    print "\t".join(t.cells)

except Exception, e:
    print 'Something went wrong : %s' % (e)
