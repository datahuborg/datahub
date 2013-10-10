import sys
sys.path.append('./gen-py')

from core.db import *

from datahub import DataHub
from datahub.constants import *
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TSocket
from thrift.transport import TTransport

'''
@author: anant bhardwaj
@date: Oct 9, 2013

DataHub Server
'''

class DataHubHandler:
  def __init__(self):
    self.con = Connection()

  def get_version(self):
    return VERSION

  def create_database(self, db_name):
    try:
      self.con.create_database(db_name)
      return True

    except:
      return False

  def drop_database(self, db_name):
    try:
      self.con.drop_database(db_name)
      return True

    except:
      return False

  def show_databases(self):
    try:
      return str(self.con.show_databases())

    except:
      return False

  def show_tables(self, db_name):
    try:
      con = Connection(db_name=db_name)
      return str(con.show_tables())

    except:
      return False

  def create_table(self, db_name, query):
    try:
      con = Connection(db_name=db_name)
      con.create_table(query)
      return True

    except:
      return False

  def drop_table(self, db_name, table_name):
    try:
      con = Connection(db_name=db_name)
      con.drop_table(table_name)
      return True

    except:
      return False

  def execute_sql(self, db_name, query, params=None):
    try:
      con = Connection(db_name=db_name)
      return str(con.execute_sql(query, params))

    except:
      return False



handler = DataHubHandler()
  
processor = DataHub.Processor(handler)
transport = TSocket.TServerSocket('localhost', 9000)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)

print 'Starting DataHub Server'
server.serve()