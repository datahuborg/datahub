#!/usr/bin/python
import cmd
import os
import shlex
import sys

from datahub.constants import *
from client.python.dh_client import DataHubClient

'''
@author: anant bhardwaj
@date: Sep 26, 2013

datahub cli interface
'''
CMD_LIST = [
    '**Any SQL Query**'
    'SHOW DATABASES',
    'SHOW TABLES',
    'USE'
]

def authenticate(login_required=True):
  def response(f):
    def print_response(self, args):
      # TODO: authentication code here
      try:
        return f(self, args)

      except Exception, e:
          self.print_line('error: %s' % str(e))

    print_response.__doc__ = f.__doc__
    return print_response        

  return response


class DatahubTerminal(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self, completekey='tab')
    self.connection = DHConnection(database=None)
    self.prompt = "datahub> "
    self.client = DataHubClient()

  @authenticate()
  def do_show(self, line):
    try:
      tokens = line.split()
      tokens = map(lambda x: x.strip(), tokens)
      if tokens[0].lower() == 'databases':
        res = self.client.list_databases(self.connection)
        self.print_result(res)
      elif tokens[0].lower() == 'tables' and self.connection.database: 
        res = self.client.list_tables(self.connection)
        self.print_result(res)
      else:
        self.default('show ' + line)

    except Exception, e:
      self.print_line('%s' % (e.message))

  @authenticate()
  def do_use(self, line):
    try:
      tokens = line.split()
      tokens = map(lambda x: x.strip(), tokens)
      self.connection.database = tokens[0]
      status =  self.client.connect_database(self.connection)
      self.print_line('%s' % ('success' if status else 'error'))
    except Exception, e:
      self.print_line('%s' % (e.message))

  @authenticate()
  def default(self, line):
    try:      
      res = self.client.execute_sql(self.connection, line, params=None)
      self.print_result(res)
    except Exception, e:
      self.print_line('%s' % (e.message))

  def do_exit(self, line):
    return True

  def print_result(self, res):
    self.print_line('')
    if res.row_count > 0:
      self.print_line('%s' % ('\t'.join(res.column_names)))
      self.print_line('%s' % (''.join(
          ['------------' for i in range(0, len(res.column_names))])))
      for t in res.tuples:
        self.print_line('%s' % ('\t'.join(t)))
    else:
      self.print_line('%s' % ('success' if res.status else 'error'))

    self.print_line('')

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
  datahub_terminal.cmdloop()

if __name__ == '__main__':
  main()