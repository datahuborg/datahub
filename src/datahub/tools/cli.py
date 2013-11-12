#!/usr/bin/python
import cmd2
import getpass
import os
import shlex
import sys

from datahub.constants import *
from client.python.dh_client import DataHubClient
from optparse import OptionParser

'''
@author: anant bhardwaj
@date: Sep 26, 2013

datahub cli interface
'''
kCmdList = [
    '** Any SQL Query **',
    'SHOW DATABASES',
    'SHOW TABLES',
    'USE <database-name>'
]


class DatahubTerminal(cmd2.Cmd):
  def __init__(self):
    usage = "--user <user-name> [--database <database-name>] [--host <host-name>] [--port <port>]"
    parser = OptionParser()
    parser.set_usage(usage)
    parser.add_option("-u", "--user", dest="user", help="DataHub username")
    parser.add_option("-H", "--host", dest="host", help="DataHub server hostname", default="datahub-experimental.csail.mit.edu")
    parser.add_option("-p", "--port", dest="port", help="DataHub server port", type="int", default=9000)
    parser.add_option("-d", "--database", dest="database", help="DataHub database")
    (options, args) = parser.parse_args()

    if not options.user:
      parser.print_usage()
      sys.exit(1)

    parser.destroy()
    password = getpass.getpass('DataHub password for %s: ' %(options.user))
    cmd2.Cmd.__init__(self, completekey='tab')
    self.client = DataHubClient(host=options.host, port=options.port)
    try:
      database = None
      if options.database:
        database=DHDatabase(name=options.database)

      self.con_params = DHConnectionParams(
          user=options.user,
          password=password,
          database=database)
      self.con = self.client.connect(self.con_params)
      self.prompt = "datahub> "
    except Exception, e:
      self.print_line('error: %s' % (e.message))
      sys.exit(1)

  def do_show(self, line):
    try:
      tokens = line.split()
      tokens = map(lambda x: x.strip(), tokens)
      if tokens[0].lower() == 'databases':
        res = self.client.list_databases(self.con)
        self.print_result(res)
      elif tokens[0].lower() == 'tables' and self.con.database.name: 
        res = self.client.list_tables(con=self.con)
        self.print_result(res)
      else:
        self.print_line('error: not connected to any database')

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_use(self, line):
    try:
      tokens = line.split()
      tokens = map(lambda x: x.strip(), tokens)
      database = DHDatabase(name=tokens[0])
      self.con_params.database = database
      self.con =  self.client.connect(self.con_params)
      self.print_line('%s' % ('success'))
    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def default(self, line):
    try:
      
      if self.con.database.name:   
        res = self.client.execute_sql(
            con=self.con, query=line, query_params=None)
        self.print_result(res)
      else:
        self.print_line('error: not connected to any database')

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_exit(self, line):
    return True

  def print_result(self, res):
    if res.row_count >= 0:
      col_names = [field.name
          for field in res.data.schema.fields]
      self.print_line('%s' % ('\t'.join(col_names)))
      self.print_line('%s' % (''.join(
          ['------------' for i in range(0, len(col_names))])))
      for row in res.data.table.rows:
        self.print_line('%s' % ('\t'.join([c.value for c in row.cells])))

      self.print_line('')
      self.print_line('%s rows returned' % (res.row_count))
    else:
      self.print_line('%s' % ('success' if res.status else 'error'))

  def do_help(self, line): 
    for cmd in CMD_LIST:
      self.print_line(cmd)

  def print_line(self, line):
    self.stdout.write(line)
    self.stdout.write('\n')

  def completedefault(self, text, line, begidx, endidx):
    pass


def main():  
  datahub_terminal = DatahubTerminal()
  sys.argv = sys.argv[:1]
  datahub_terminal.cmdloop()


if __name__ == '__main__':
  main()
