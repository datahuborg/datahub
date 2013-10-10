#!/usr/bin/python
import cmd
import os
import shlex
import sys

from client.python.dh_client import DataHubClient

'''
@author: anant bhardwaj
@date: Sep 26, 2013

datahub cli interface
'''
CMD_LIST = [
    'CREATE DATABASE',
    'CREATE TABLE',
    'DROP DATABASE',
    'DROP TABLE',
    'SHOW DATABASES',
    'SHOW TABLES',
    'SELECT',
    'USE'
]

COMMIT_TOKENS = [
    'create',
    'insert',
    'update',
    'delete',
    'alter',
    'drop'
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
    self.session = {}
    self.prompt = "datahub> "
    self.client = DataHubClient()

  @authenticate()
  def do_show(self, line):
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    if tokens[0].lower() == 'databases':
      res = self.client.show_databases()
      self.print_line('%s' % (res))
    elif tokens[0].lower() == 'tables' and 'database' in self.session:
      db = self.session['database']    
      res = self.client.show_tables(db)
      self.print_line('%s' % (res))
    else:
      self.default('show ' + line)

  @authenticate()
  def do_use(self, line):
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    self.session['database'] = tokens[0]
    self.print_line('connected to: %s' % (self.session['database']))

  @authenticate()
  def do_drop(self, line):
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    if tokens[0].lower() == 'database':
      res = self.client.drop_database(tokens[1])
      self.print_line('%s' % (res))
    else:
      self.default('drop ' + line)

  @authenticate()
  def do_create(self, line):
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    if tokens[0].lower() == 'database':
      res = self.client.create_database(tokens[1])
      self.print_line('%s' % (res))
    else:
      self.default('create ' + line)

  @authenticate()
  def default(self, line):
    commit = False
    tokens = line.split()
    if tokens[0].lower() in COMMIT_TOKENS:
      commit = True

    if 'database' in self.session:
        db = self.session['database']
        res = self.client.execute_sql(db, line, commit=commit)
    else:
      res = '** not connected to any database'

    self.print_line('%s' % (res))

  def do_exit(self, line):
    return True

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