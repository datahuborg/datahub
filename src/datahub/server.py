#!/usr/bin/python
import os
import sys
sys.path.append('./gen-py')

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
      dh_database = DHDatabase()
      if dh_con_params.database:
        dh_database.name = dh_con_params.database.name

      con = Connection(
          user=dh_con_params.user,
          password=dh_con_params.password,
          db_name=dh_database.name)

      # hack for access control -- implement proper session management later
      self.sessions[dh_con_params.user] = con
      dh_con = DHConnection(user=dh_con_params.user, database=dh_database)
      return dh_con
    except Exception, e:
      raise DHException(message=str(e))
    
  def list_databases(self, dh_con):
    try:
      con = self.sessions[dh_con.user]
      res = con.list_databases()
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def list_tables(self, dh_con):
    try:
      con = self.sessions[dh_con.user]
      res = con.list_tables()
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def execute_sql(self, dh_con, query, query_params=None):
    try:
      con = self.sessions[dh_con.user]
      res = con.execute_sql(query, query_params)
      return construct_query_result(res)
    except Exception, e:
      raise DHException(message=str(e))

  def load(self, dh_con, url):
    db_name, table_name = url.split('.')
    try:
      con = self.sessions[dh_con.user]
      res = con.execute_sql('SELECT * from %s' % (table_name))
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
