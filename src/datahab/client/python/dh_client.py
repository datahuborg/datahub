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


def main():
  client = DataHubClient()
  print client.get_version()

if __name__ == '__main__':
  main()