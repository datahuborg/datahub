import sys
import pyclbr # Module to get classes from files

"""
@author: Jesika Haria 
@date: October 30, 2013

ORM Parser (Python)
"""

# Imports - should go in helper function
importStatement = 'from '
filename = sys.argv[1].split('.')[0]
print 'filename is ', filename
importStatement += filename + ' import *'
exec(importStatement) #from sample_models import *

# String to be generated: create table person (id integer, name varchar(20))
query = ''

classList = pyclbr.readmodule(filename).keys() # Get list of all classes defined as strings
print 'classList ', classList 

for classItem in classList:
  query += 'create table '
  query += classItem + '('

  objectClass = eval(classItem) # get the class defined
  print 'objectClass ', objectClass
  classAttrs = [attr for attr in dir(objectClass) if not callable(attr) and not attr.startswith("__")]
  print 'classAttrs ', classAttrs

  for attrString in classAttrs:
    query += attrString + ' '

    objAttr = getattr(objectClass, attrString)
    print 'objAttr ', objAttr
    
    # This should go in a helper function
    if objAttr.__class__.__name__ == 'CharField':
      query += 'varchar('
    elif objAttr.__class__.__name__ == 'IntegerField':
      query += 'int '
    elif objAttr.__class__.__name__ == 'DatetimeField':
      query += 'datetime '
    elif objAttr.__class__.__name__ == 'BooleanField':
      query += 'boolean '

    fieldAttrs = [attr for attr in dir(objAttr) if not callable(attr) and not attr.startswith("__")]
    print 'fieldAttrs ', fieldAttrs

    for fieldAttrString in fieldAttrs:
      fieldAttr = getattr(objAttr, fieldAttrString)
      print 'fieldAttr ', fieldAttr
      if fieldAttrString == 'size':
        query += str(fieldAttr)+')'

    if classAttrs.index(attrString) != len(classAttrs)-1:
      query += ', '  
  query += '); '


print 'and the final result is the following query: ', query
