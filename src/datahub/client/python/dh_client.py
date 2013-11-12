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
  def __init__(self, host, port):
    try:
      transport = TSocket.TSocket(host, port)
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

  def connect(self, con_params):
    self.transport.open()
    con = self.client.connect(con_params)
    self.transport.close()
    return con

  def list_repos(self, con):
    self.transport.open()
    res = self.client.list_repos(con)
    self.transport.close()
    return res

  def list_tables(self, con, repo):
    self.transport.open()
    res = self.client.list_tables(con, repo)
    self.transport.close()
    return res

  def execute_sql(self, con, query, query_params=None):
    self.transport.open()
    res = self.client.execute_sql(con, query, query_params)
    self.transport.close()
    return res

  def load(self, con, url):
    self.transport.open()
    res = self.client.load(con, url)
    self.transport.close()
    return res


def test():
  client = DataHubClient(host='datahub-experimental.csail.mit.edu', port=9000)
  print client.get_version()
  con_params = DHConnectionParams(user='anant', password='anant')
  con = client.connect(con_params=con_params)
  print client.list_repos(con=con)

  try:
    print client.execute_sql(con=con, query=''' drop schema test ''')
    print client.list_repos(con=con)
  except Exception, e:
    print e.message

  print client.execute_sql(con=con, query=''' create schema test ''')
  print client.list_repos(con=con)

  print client.list_tables(con=con, repo='test')
  print client.execute_sql(con=con,
      query=''' create table person (id integer, name varchar(20)) ''')
  print client.list_tables(con=con, repo='test')
  print client.execute_sql(con=con, query=''' select * from person ''')
  print client.execute_sql(con=con,
      query=''' insert into person values (1, 'anant') ''')
  print client.execute_sql(con=con, query=''' select * from person ''')

if __name__ == '__main__':
  test()
