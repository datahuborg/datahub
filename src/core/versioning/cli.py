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
    'init':     'init <repo> <user>           -- initialize versioning for a repo',
    'clone':    'clone <v_id>           -- clone the table (version=HEAD)',
    'checkout': 'checkout <v>    -- check out version v_id',
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
      argv = args.strip().split()
      
      
      if len(argv) == 0:
        user = 'test'
        repo = 'test'
        self.print_line('Using test user and repo')
      elif len(argv) == 1:  
        user = 'test'
        repo = argv[0]
        self.print_line('Using test user and repo: %s' % repo)
      elif len(argv) == 2:  
        user = argv[1]
        repo = argv[0]
        self.print_line('Using user:%s and repo: %s' % (user,repo))        
      
      self.session.init(user, repo)

    except Exception, e:
      self.print_line('error: %s' % (e.message))

  @authenticate()
  def do_clone(self, args):
    try:
      v_id = int(args.strip())

      if v_id == '':
        self.do_help('clone')
      
      self.session.clone(v_id)

    except Exception, e:
      self.print_line('error: %s' % (e.message))


  @authenticate()
  def do_co(self, args):
    self.do_checkout(args)

  @authenticate()
  def do_checkout(self, args):
    try:
      argv = args.strip().split()

      if len(argv) < 1:
        self.do_help('checkout')
      
      v_id = argv[0]
      
      result = self.session.checkout( v_id)
      if result:
        self.print_line("checkout v_id %s was succesful" % v_id)
      else:
        self.print_line("checkout v_id %s was not succesful, does the version exist?" % v_id)
        

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
      
      self.print_line('current v_id:%s'% self.session.current_version) 
      self.print_line('v_id\tname') 
      for b in branches:
        self.print_line('%s\t%s ' % (b[0],b[1]))
    except Exception, e:
      self.print_line('error: %s' % (e.message))
  

      
  @authenticate()
  def do_sql(self, args):
    try:
      query = args.strip()  
      self.print_line(str(self.session.sql(query)))
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
