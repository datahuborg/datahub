#!/usr/bin/python

from client.python.dh_client import DataHubClient
from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code accesing DataHub APIs
'''


# conect to DataHub
client = DataHubClient('datahub-experimental.csail.mit.edu', 9000)
con_params = DHConnectionParams(user='anant', password='anant')
con = client.connect(con_params=con_params)

# list databases
print client.list_repos(con=con)

# delete if database named 'test' already exists
try:
  print client.execute_sql(con=con, query=''' drop schema test cascade''')
  print client.list_repos(con=con)
except Exception, e:
  print e.message
  
# create a database named 'test'
print client.execute_sql(con=con, query=''' create schema test ''')
print client.list_repos(con=con)


# create a table named 'person'
print client.list_tables(con=con, repo='test')
print client.execute_sql(con=con,
    query=''' create table test.person (id integer, name varchar(20)) ''')
print client.list_tables(con=con, repo='test')

# insert/delete/update records
print client.execute_sql(con=con,
    query=''' insert into test.person values (1, 'anant') ''')
print client.execute_sql(con=con,
    query=''' insert into test.person values (2, 'david') ''')
print client.execute_sql(con=con,
    query=''' insert into test.person values (3, 'sam') ''')
print client.execute_sql(con=con, query=''' select * from person ''')
