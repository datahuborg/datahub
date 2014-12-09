#!/usr/bin/python
import cmd
import os
import shlex
import sys

'''
@author: anant bhardwaj
@date: Dec 8, 2014

versioning cli interface
'''
CMD_LIST = [
    'clone <table_name>'
    'checkout <table_name> [version_no]'
    'sql <query>',
    'commit',
    'stash',
    'diff [version 1] [version 2]'
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


class CmdTerminal(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self, completekey='tab')
    self.prompt = "datahub> "

  @authenticate()
  def do_clone(self, args):
    try:
      table_name = args.strip()
      # do clone_table

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_checkout(self, args):
    try:
      argv = args.strip().split()
      table_name = argv[0]

      if len(argv) > 1:
        version = argv[1]

      # execute checkout(table_name, version=version)
      # default is HEAD

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_commit(self, args):
    try:
      table_name = args.strip()
      # execute commit_table

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_stash(self, args):
    try:
      # execute stash
      pass

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_diff(self, args):
    try:
      argv = args.strip().split()
      
      if len(argv) > 0:
        version_1 = argv[0]

      if len(argv) > 1:
        version_2 = argv[1]

      # execute diff(version_1, version_2)
      # default version_1 is HEAD
      # default version_2 is USER's uncommited version

    except Exception, e:
      self.print_line('error: %s' % (e.message))
  

  @authenticate()
  def do_sql(self, args):
    try:
      query = args.strip()  
      # execute_sql(query=query)
      # print result
    except Exception, e:
      self.print_line('error: %s' % (e.message))

  def do_exit(self, args):
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
  cmd_terminal = CmdTerminal()
  cmd_terminal.cmdloop()

if __name__ == '__main__':
  main()
