from sysapi import SystemVersioning

'''
@author: anant bhardwaj
@date: Dec 8, 2014

versioning session manager
'''

class DataHubSession:
  def __init__(self):
    self.sv = SystemVersioning()
  
  #TODO
  def clone(self, table_name):
    pass

  #TODO
  def checkout(self, v_id):
    pass
  
  #TODO
  def stash(self):
    pass

  #TODO
  def commit(self):
    pass

  #TODO
  def diff(self, v_id):
    pass

  #TODO
  def sql(self, query):
    pass
    
  
    
    