import sys
sys.path.append('./gen-py')

from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code for using DataHub ORMs
'''

class Faculty:
  id = DHField(type=DHType.Boolean)
  name = DHField(type=DHType.String)

f = Faculty()
print f.id, f.name