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
      protocol = TBinaryProtocol.TBinaryProtocol(transport)
      self.client = DataHub.Client(protocol)
    except Thrift.TException, tex:
      print '%s' % (tex.message)

  def get_version(self):
    self.transport.open()
    version = self.client.get_version()
    self.transport.close()
    return version

  def create_database(self, db_name):
    self.transport.open()
    res = self.client.create_database(db_name)
    self.transport.close()
    return res

  def drop_database(self, db_name):
    self.transport.open()
    res = self.client.drop_database(db_name)
    self.transport.close()
    return res

  def show_databases(self):
    self.transport.open()
    res = self.client.show_databases()
    self.transport.close()
    return res

  def show_tables(self, db_name):
    self.transport.open()
    res = self.client.show_tables(db_name)
    self.transport.close()
    return res

  def create_table(self, db_name, query):
    self.transport.open()
    res = self.client.create_table(db_name, query)
    self.transport.close()
    return res

  def drop_table(self, db_name, table_name):
    self.transport.open()
    res = self.client.drop_table(db_name, table_name)
    self.transport.close()
    return res

  def execute_sql(self, db_name, query, params=None):
    self.transport.open()
    res = self.client.execute_sql(db_name, query, params)
    self.transport.close()
    return res


def main():
  client = DataHubClient()
  print client.get_version()
  print client.drop_database('datahub')
  print client.show_databases()
  print client.create_database('datahub')
  print client.show_databases()
  print client.show_tables('datahub')
  print client.create_table('datahub', 'create table test(id integer, name varchar(20))')
  print client.show_tables('datahub')

if __name__ == '__main__':
  main()