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

try:
  transport = TSocket.TSocket("localhost", 9000)
  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = DataHub.Client(protocol)

  transport.open()

  print client.get_version()

  transport.close()

except Thrift.TException, tex:
  print '%s' % (tex.message)