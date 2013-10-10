import sys
sys.path.append('./gen-py')

from datahub.tutorials.thrift_sample.constants import *
from datahub.tutorials.thrift_sample import ttypes
from types import ClassType

'''
@author: anant bhardwaj
@date: Oct 9, 2013

Sample Schema Parsing (Thrift IDL)
'''

dept = Department(id=1, name='MIT CSAIL')
faculty = Faculty(id=1, name='Sam Madden', dept=dept, sex=Sex.MALE)


classes = [getattr(ttypes, x) for x in dir(ttypes) if isinstance(getattr(ttypes, x), ClassType)]
for c in classes:
  if hasattr(c, 'thrift_spec'):
    for k in c.thrift_spec:
      print k
    print "======================"