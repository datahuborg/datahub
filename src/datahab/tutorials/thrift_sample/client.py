import sys
sys.path.append('./gen-py')
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from datahub.tutorials.thrift_sample.constants import *
from datahub.tutorials.thrift_sample import UniversityInfo

'''
@author: anant bhardwaj
@date: Oct 9, 2013

Sample Client Code (Thrift)
'''

dept = Department(id=1, name='MIT CSAIL')
faculty = Faculty(id=1, name='Sam Madden', dept=dept, sex=Sex.MALE)

transport = TSocket.TSocket("localhost", 9090)
transport.open()
protocol = TBinaryProtocol.TBinaryProtocol(transport)

service = UniversityInfo.Client(protocol)

print service.get_faculties()
print service.get_departments()