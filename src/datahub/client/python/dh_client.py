import sys
sys.path.append('./gen-py')

from datahub import DataHub
from datahub.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Client (Python)
'''

class DataHubClient:
  def __init__(self):
    try:
      transport = TSocket.TSocket("localhost", 9000)
      self.transport = TTransport.TBufferedTransport(transport)
      protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
      self.client = DataHub.Client(protocol)
    except Thrift.TException, tex:
      print '%s' % (tex.message)

  def get_version(self):
    self.transport.open()
    version = self.client.get_version()
    self.transport.close()
    return version

  def list_databases(self, con):
    self.transport.open()
    res = self.client.list_databases(con)
    self.transport.close()
    return res

  def list_tables(self, con):
    self.transport.open()
    res = self.client.list_tables(con)
    self.transport.close()
    return res

  def execute_sql(self, con, query, params=None):
    self.transport.open()
    res = self.client.execute_sql(con, query, params)
    self.transport.close()
    return res


def test():
  client = DataHubClient()
  print client.get_version()
  con = DHConnection(database=None, user='anantb')
  print client.list_databases(con)

  try:
    print client.execute_sql(con, 'drop database test')
    print client.list_databases(con)
  except:
    pass

  print client.execute_sql(con, 'create database test')
  print client.list_databases(con)

  con = DHConnection(database='test', user='anantb')
  print client.list_tables(con)
  print client.execute_sql(con, 'create table person(id integer, name varchar(20))')
  print client.list_tables(con)

if __name__ == '__main__':
  test()