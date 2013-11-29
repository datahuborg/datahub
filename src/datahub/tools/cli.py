#!/usr/bin/python
import cmd2
import getpass
import os
import shlex
import sys

from datahub import DataHub
from datahub.constants import *

from thrift import Thrift
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket
from thrift.transport import TTransport

from optparse import OptionParser

'''
@author: anant bhardwaj
@date: Sep 26, 2013

datahub cli interface
'''
kCmdList = [
    '** Any SQL Query **',
    'mkrepo <repo-name> \t -- to create a new repository',
    'ls \t\t\t -- to list repositories',
    'ls <repo-name> \t\t -- to list tables in a repository',
    'rm <repo-name> \t\t -- to remove a repository',
]


class DatahubTerminal(cmd2.Cmd):
  def __init__(self):
    usage = "--user <user-name> [--host <host-name>] [--port <port>]"
    parser = OptionParser()
    parser.set_usage(usage)
    parser.add_option("-u", "--user", dest="user", help="DataHub username")
    parser.add_option("-H", "--host", dest="host", help="DataHub server hostname", default="datahub-experimental.csail.mit.edu")
    parser.add_option("-p", "--port", dest="port", help="DataHub server port", type="int", default=9000)
    (options, args) = parser.parse_args()

    if not options.user:
      parser.print_usage()
      sys.exit(1)

    parser.destroy()
    password = getpass.getpass('DataHub password for %s: ' %(options.user))
    cmd2.Cmd.__init__(self, completekey='tab')
    transport = TSocket.TSocket(options.host, options.port)
    self.transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = DataHub.Client(protocol)
    self.transport.open()
    try:
      self.con_params = DHConnectionParams(
          user=options.user,
          password=password)
      self.con = self.client.connect(self.con_params)
      self.prompt = "datahub> "
    except Exception, e:
      self.print_line('error: %s' % (e.message))
      sys.exit(1)

  def do_ls(self, line):
    try:
      repo = line.strip()
      if repo != '':
        res = self.client.list_tables(con=self.con, repo=repo)
        self.print_result(res)
      else:
        res = self.client.list_repos(self.con)
        self.print_result(res)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_mkrepo(self, line):
    try:
      repo = line.strip()
      if repo != '':
        res = self.client.execute_sql(
            con=self.con,
            query = 'CREATE SCHEMA %s' %(repo),
            query_params = None)
        self.print_result(res)
      else:
        self.print_line("invalid repo name: '%s'" % (repo))

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_rm(self, line):
    try:
      repo = line.strip()
      if repo != '':
        res = self.client.execute_sql(
            con=self.con,
            query = 'DROP SCHEMA %s' %(repo),
            query_params = None)
        self.print_result(res)
      else:
        self.print_line("invalid repo name: '%s'" % (repo))

    except Exception, e:
      self.print_line('error: %s' % (e.message))


  def default(self, line):
    try:      
      res = self.client.execute_sql(
          con=self.con,
          query=line,
          query_params=None)
      self.print_result(res)
    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_exit(self, line):
    self.transport.close()
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
    for cmd in kCmdList:
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
