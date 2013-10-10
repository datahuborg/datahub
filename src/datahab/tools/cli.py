#!/usr/bin/python
import cmd
import os
import shlex
import sys

from client.python.client import DataHubClient

'''
@author: anant bhardwaj
@date: Sep 26, 2013

datahub cli interface
'''

def authenticate(login_required=True):
  def response(f):
    def print_response(self, args):
      # TODO: authentication code here
      try:
          return f(self, *args)
      except TypeError, e:
          self.stdout.write(str(e) + '\n')
      except Error, e:
          self.stdout.write('Error: %s\n' % str(e))

    print_response.__doc__ = f.__doc__
    return print_response        
      
  return response


class DatahubTerminal(cmd.Cmd):
  def __init__(self):
    cmd.Cmd.__init__(self)
    self.sess = ""
    self.prompt = "datahub> "
    self.client = DataHubClient()

  @authenticate()
  def do_info(self):
    """prints version number."""
    version = self.client.get_version()
    self.stdout.write('%s\n' % (version))

  @authenticate()
  def do_exit(self):
    """exits the datahub shell."""
    return True

  @authenticate()
  def do_help(self):
    cmd_list = dir(self)
    cmd_names = []
    for name in cmd_list:
      if name[:3] == 'do_':
        cmd_names.append(name[3:])
    cmd_names.sort()
    for cmd_name in cmd_names:
      f = getattr(self, 'do_' + cmd_name)
      if f.__doc__:
        self.stdout.write('%s: %s\n' % (cmd_name, f.__doc__))

  def do_EOF(self, line):
    self.stdout.write('\n')
    return True

  def parse_line(self, line):
    parts = shlex.split(line)
    if len(parts) == 0:
      return None, None, line
    else:
      return parts[0], parts[1:], line


def main():
  datahub_terminal = DatahubTerminal()
  datahub_terminal.cmdloop()

if __name__ == '__main__':
  main()