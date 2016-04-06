#!/usr/bin/python
from datahub import DataHub
from service.handler import DataHubHandler

from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Server (TCP Mode)
'''

handler = DataHubHandler()

processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('0.0.0.0', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(
    processor, transport, tfactory, pfactory)

print('Starting DataHub Server')
server.serve()
