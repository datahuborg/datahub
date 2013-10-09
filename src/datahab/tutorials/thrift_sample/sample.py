import sys
sys.path.append('./gen-py')
from datahub.tutorials.thrift_sample.constants import *

'''
@author: anant bhardwaj
@date: Oct 9, 2013

Thrift Sample Code
'''

dept = Department(id=1, name='MIT CSAIL')
faculty = Faculty(id=1, name='Sam Madden', dept=dept, sex=Sex.MALE)

print faculty.dept
