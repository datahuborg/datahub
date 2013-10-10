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

def authenticate(login_required=True):
  def response(f):
    def print_response(self, args):
      # TODO: authentication code here
      try:
        return f(self, args)

      except Exception, e:
          self.print_line('Error: %s' % str(e))

    print_response.__doc__ = f.__doc__
    return print_response        

  return response


class DatahubTerminal(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self)
    self.session = {'user': None, 'database': None}
    self.prompt = "datahub> "
    self.client = DataHubClient()

  @authenticate()
  def do_show(self, line):
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    if tokens[0].lower() == 'databases':
      res = self.client.show_databases()
    elif tokens[0].lower() == 'tables':
      db = self.session['database']
      if db:
        res = self.client.show_tables(db)
    else:
      pass

    self.print_line('%s' % (res))

  @authenticate()
  def do_use(self, line):
    res = None
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    self.session['database'] = tokens[0]
    self.print_line('connected to: %s' % (self.session['database']))

  @authenticate()
  def do_drop(self, line):
    res = None
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    if tokens[0].lower() == 'database':
      res = self.client.drop_database(tokens[1])
    elif tokens[0].lower() == 'table':
      db = self.session['database']
      if db:
        res = self.client.drop_table(db, tokens[1])
    else:
      pass

    self.print_line('%s' % (res))

  @authenticate()
  def do_create(self, line):
    res = None
    tokens = line.split()
    tokens = map(lambda x: x.strip(), tokens)
    if tokens[0].lower() == 'database':
      res = self.client.create_database(tokens[1])
    elif tokens[0].lower() == 'table':
      db = self.session['database']
      if db:
        res = self.client.create_table(db, 'create ' + ' '.join(tokens))
    else:
      pass

    self.print_line('%s' % (res))

  def do_exit(self, line):
    return True

  def do_help(self, line): 
    for cmd in CMD_LIST:
      self.print_line(cmd)

  def print_line(self, line):
    self.stdout.write(line)
    self.stdout.write('\n')

  def completedefault(text, line, begidx, endidx):
    print text, line, begidx, endidx



def main():
  datahub_terminal = DatahubTerminal()
  datahub_terminal.cmdloop()

if __name__ == '__main__':
  main()