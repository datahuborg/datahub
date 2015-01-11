#!/usr/bin/python
import cmd
import os
import shlex
import sys

from datahub_session import DataHubSession

'''
@author: anant bhardwaj
@date: Dec 8, 2014

versioning cli interface
'''
CMD_LIST = {
    'init':     'init <table>            -- initialize versioning for the table',
    'clone':    'clone <table>           -- clone the table (version=HEAD)',
    'checkout': 'checkout <table> <v>    -- check out version v of the table',
    'sql':      'sql <query>             -- run a sql command on the checked out version',
    'commit':   'commit <table>          -- commit all the local changes to the table',
    'stash':    'stash <table>           -- undo all uncommitted changes to the table',
    'diff':     'diff <table> [v]        -- diff version v and HEAD of the table'
}

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


class CmdTerminal(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self, completekey='tab')
    self.session = DataHubSession()
    self.prompt = "datahub> "

  @authenticate()
  def do_init(self, args):
    try:
      table_name = args.strip()

      if table_name == '':
        self.do_help('init')
      
      self.session.init(table_name)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_clone(self, args):
    try:
      table_name = args.strip()

      if table_name == '':
        self.do_help('clone')
      
      self.session.clone(table_name)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_checkout(self, args):
    try:
      argv = args.strip().split()

      if len(argv) < 2:
        self.do_help('checkout')
      
      table_name = argv[0]
      v_id = argv[1]
      
      self.session.checkout(table_name, v_id)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_commit(self, args):
    try:
      table_name = args.strip()

      if table_name == '':
        self.do_help('commit')
      
      self.session.commit(table_name)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_stash(self, args):
    try:
      table_name = args.strip()

      if table_name == '':
        self.do_help('stash')
      
      self.session.stash(table_name)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_diff(self, args):
    try:
      argv = args.strip().split()
      table_name = argv[0]

      if table_name == '':
        self.do_help('diff')
      v_id = argv[1] if len(argv) > 1 else None
      self.session.diff(table_name, v_id)
    except Exception, e:
      self.print_line('error: %s' % (e.message))
  
  @authenticate()
  def do_branch(self, args):
    try:
      argv = args.strip()  
      branches = self.session.branch(argv)
      self.print_line('v_id\tname') 
      for b in branches:
        self.print_line('%s\t%s ' % (b[0],b[1]))
    except Exception, e:
      self.print_line('error: %s' % (e.message))
  

      
  @authenticate()
  def do_sql(self, args):
    try:
      query = args.strip()  
      self.session.sql(query)
    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_exit(self, args):
    return True

  def do_help(self, args):
    if args in CMD_LIST.keys():
      self.print_line(CMD_LIST[args])
      return

    for cmd in CMD_LIST:
      self.print_line(CMD_LIST[cmd])

  def print_line(self, line):
    self.stdout.write(line)
    self.stdout.write('\n')

  def completedefault(self, text, line, begidx, endidx):
    pass


def main():
  cmd_terminal = CmdTerminal()
  cmd_terminal.cmdloop()

if __name__ == '__main__':
  main()
