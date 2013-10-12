import sys
sys.path.append('./gen-py')

from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code for using DataHub ORMs
'''

Faculty = DHSchema(
    name = 'faculty',
    fields = [
        DHField(name='id', type=DHType.Boolean),
        DHField(name='name', type=DHType.Text)
    ]
  )


print Faculty