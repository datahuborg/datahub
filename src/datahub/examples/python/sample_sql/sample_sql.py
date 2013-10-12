#!/usr/bin/python

from client.python.dh_client import DataHubClient
from datahub.constants import *

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code accesing DataHub APIs
'''


# conect to DataHub
client = DataHubClient()
con_params = DHConnectionParams(user=None, password=None, database=None)
con = client.connect(con_params=con_params)

# list databases
print client.list_databases(con=con)

# delete if database named 'test' already exists
try:
  print client.execute_sql(con=con, query=''' drop database test ''')
  print client.list_databases(con=con)
except Exception, e:
  print e.message
  
# create a database named 'test'
print client.execute_sql(con=con, query=''' create database test ''')
print client.list_databases(con=con)

# connect to the database 'test' and open the database
database = DHDatabase(name='test')
con = client.open_database(con=con, database=database)

# create a table named 'person'
print client.list_tables(con=con)
print client.execute_sql(con=con,
    query=''' create table person (id integer, name varchar(20)) ''')
print client.list_tables(con=con)

# insert/delete/update records
print client.execute_sql(con=con,
    query=''' insert into person values (1, 'anant') ''')
print client.execute_sql(con=con,
    query=''' insert into person values (2, 'david') ''')
print client.execute_sql(con=con,
    query=''' insert into person values (3, 'sam') ''')
print client.execute_sql(con=con, query=''' select * from person ''')
