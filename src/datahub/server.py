import sys
sys.path.append('./gen-py')

from core.db import *

from datahub import DataHub
from datahub.constants import *
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Server
'''

def construct_query_result(res):
  query_result = QueryResult(
      status = res['status'],
      row_count = res['row_count'],
      column_types = res['column_types'],
      column_names = res['column_names'],
      tuples = res['tuples'])

  return query_result


class DataHubHandler:
  def __init__(self):
    pass

  def get_version(self):
    return VERSION

  def list_databases(self, con):  
    try:
      con = Connection()
      res = con.list_databases()
      return construct_query_result(res)

    except Exception, e:
      raise DBException(message=str(e))
    

  def list_tables(self, con):
    try:
      con = Connection(db_name=con.database)
      res = con.list_tables()
      return construct_query_result(res)

    except Exception, e:
      raise DBException(message=str(e))

  def execute_sql(self, con, query, params=None):
    try:
      con = Connection(db_name=con.database)
      res = con.execute_sql(query, params)
      return construct_query_result(res)

    except Exception, e:
      raise DBException(message=str(e))

handler = DataHubHandler()
  
processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting DataHub Server'
server.serve()