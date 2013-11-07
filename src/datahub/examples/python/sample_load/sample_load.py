#!/usr/bin/python

from client.python.dh_client import DataHubClient
from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code accesing DataHub APIs
'''


# conect to DataHub
client = DataHubClient('localhost', 9000)
con_params = DHConnectionParams(user='postgres', password='postgres', database=DHDatabase(name='postgres'))
con = client.connect(con_params=con_params)

result = client.load(con=con, url='demo.person')

for row in result.data.table.rows:
  print '\t'.join([c.value for c in row.cells])
  print '\n'