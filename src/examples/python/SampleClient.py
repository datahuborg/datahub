#!/usr/bin/python

from gen_py.datahub import DataHub
from gen_py.datahub.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import THttpClient
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample Python client for DataHub
'''
username = "USERNAME"
password = "PASSWORD"
repo = "REPO"
table = "TABLE"

try:
  # Before running you will need to populate the above variables
  # and create a corresponding repo and table in your datahub acount
  print "Trying to connect to datahub with the following credentials..."
  print "\tu: " +username + "\tp: " + password
  print "\trepo: " + repo + "\ttable:" + table
  transport = THttpClient.THttpClient('http://datahub.csail.mit.edu/service')
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DataHub.Client(protocol)
  
  print "Version: %s" %(client.get_version())
  
  # open connection
  con_params = ConnectionParams(user=username, password=password)
  con = client.open_connection(con_params=con_params)


  # execute a query
  query = "select * from " + username + "." + repo + "." + table
  print "\nTrying to execute the followin query:\t" + query + "..."

  res  = client.execute_sql(
      con=con,
      query=query,
      query_params=None)

  # print field names
  print "\t".join(res.field_names)
  
  # print tuples
  for t in res.tuples:
    print "\t".join(t.cells)

except Exception, e:
    print 'Something went wrong : %s' % (e)
