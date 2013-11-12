#!/usr/bin/python
import hashlib

from core import manager
from core.db.connection import *

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
  table = DHTable(rows=[
      DHRow(
          cells=[DHCell(value=bytes(val)) for val in t]
      ) for t in res['tuples']
  ])

  schema = DHSchema(fields=[
      DHField(
          name=res['column_names'][i],
          type=DHType.Binary
      ) for i in range(0, len(res['column_names']))
  ])

  query_result = DHQueryResult(
      status=res['status'],
      row_count=res['row_count'],
      data=DHData(
          table=table, schema=schema
      )
  )

  return query_result


class DataHubHandler:
  def __init__(self):
    self.sessions={}
    pass

  def get_version(self):
    return VERSION

  def connect(self, dh_con_params):  
    try:
      con = Connection(
          user=dh_con_params.user,
          password=hashlib.sha1(dh_con_params.password).hexdigest(),
          db_name=dh_con_params.user)

      dh_con = DHConnection(user=dh_con_params.user)
      return dh_con
    except Exception, e:
      raise DHException(message=str(e))
    
  def list_repos(self, dh_con):
    try:
      res = manager.list_repos(username=dh_con.user)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def list_tables(self, dh_con, repo):
    try:
      res = manager.list_tables(dh_con.user, repo)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def execute_sql(self, dh_con, query, query_params=None):
    try:
      res = manager.execute_sql(dh_con.user, query, query_params)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def load(self, dh_con, url):
    try:
      qry = 'SELECT * from %s' % (url)
      res = manager.execute_sql(dh_con.user, qry)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))


handler = DataHubHandler()
  
processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('0.0.0.0', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(
    processor, transport, tfactory, pfactory)

print 'Starting DataHub Server'
server.serve()
