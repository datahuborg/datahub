#!/usr/bin/python
import cmd2
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
kCmdList = [
    '** Any SQL Query **',
    'SHOW DATABASES',
    'SHOW TABLES',
    'USE <database-name>'
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


class DatahubTerminal(cmd2.Cmd):
  def __init__(self):
    cmd2.Cmd.__init__(self, completekey='tab')
    self.client = DataHubClient()
    con_params = DHConnectionParams(user=None, password=None, database=None)
    self.con = self.client.connect(con_params)
    self.prompt = "datahub> "

  @authenticate()
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

  @authenticate()
  def do_use(self, line):
    try:
      tokens = line.split()
      tokens = map(lambda x: x.strip(), tokens)
      database = DHDatabase(name=tokens[0])
      self.con =  self.client.open_database(con=self.con, database=database)
      self.print_line('%s' % ('success'))
    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def default(self, line):
    try:      
      res = self.client.execute_sql(
          con=self.con, query=line, query_params=None)
      self.print_result(res)
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
  datahub_terminal.cmdloop()

if __name__ == '__main__':
  main()