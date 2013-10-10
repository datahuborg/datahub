import sys
sys.path.append('./gen-py')

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

class DataHubHandler:
  def get_version(self):
    return VERSION


handler = DataHubServer()
  
processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting DataHub Server'
server.serve()