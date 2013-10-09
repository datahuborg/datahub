import sys
sys.path.append('./gen-py')

from datahub.tutorials.thrift_sample import UniversityInfo
from datahub.tutorials.thrift_sample.constants import *
from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

Sample Client Code (Thrift)
'''

try:
  transport = TSocket.TSocket("localhost", 9000)
  transport = TTransport.TBufferedTransport(transport)

  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = UniversityInfo.Client(protocol)

  transport.open()

  print client.get_faculties()
  print client.get_departments()

  transport.close()

except Thrift.TException, tex:
  print '%s' % (tex.message)