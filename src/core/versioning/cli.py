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
    'clone':    'clone <table_name>   -- clone a table with HEAD as the ID',
    'checkout': 'checkout <ID>        -- checkout a table with a different ID',
    'sql':      'sql <query>          -- run a sql command on the checked out version',
    'commit':   'commit               -- commits all the local changes',
    'stash':    'stash                -- undo all local changes',
    'diff':     'diff [ID]            -- diff with the HEAD or a a ID'
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
      v_id = args.strip()

      if v_id == '':
        self.do_help('checkout')
      
      self.session.checkout(v_id)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_commit(self, args):
    try:
      self.session.commit()

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_stash(self, args):
    try:
      self.session.stash()

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_diff(self, args):
    try:
      argv = args.strip()      
      v_id = argv if argv != '' else None

      self.session.diff(v_id)
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
