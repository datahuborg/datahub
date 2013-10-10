import sys
sys.path.append('./gen-py')

from datahub.tutorials.thrift_sample import UniversityInfo
from datahub.tutorials.thrift_sample.constants import *
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

Sample Server Code (Thrift)
'''

class SampleHandler:
  def get_faculties(self):
    dept = Department(id=1, name='MIT CSAIL')
    faculty = Faculty(id=1, name='Sam Madden', dept=dept, sex=Sex.MALE)
    return [faculty]

  def get_departments(self):
    dept = Department(id=1, name='MIT CSAIL')
    return [dept]


handler = SampleHandler()
  
processor = UniversityInfo.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting server'
server.serve()