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
  # Create the table
  query += 'CREATE TABLE '
  query += classItem + '('

  # Get the class defined 
  objectClass = eval(classItem)
  print 'objectClass ', objectClass
  classAttrs = [attr for attr in dir(objectClass) if not callable(attr) and not attr.startswith("__")]
  print 'classAttrs ', classAttrs

  # Iterate over class attributes (fields)
  for attrString in classAttrs:
    query += attrString + ' '

    objAttr = getattr(objectClass, attrString)
    print 'objAttr ', objAttr
    
    # Parse by field
    if objAttr.__class__.__name__ == 'CharField':
      query += 'varchar('
    elif objAttr.__class__.__name__ == 'IntegerField':
      query += 'int '
    elif objAttr.__class__.__name__ == 'DatetimeField':
      query += 'datetime '
    elif objAttr.__class__.__name__ == 'BooleanField':
      query += 'boolean '
    elif objAttr.__class__.__name__ == 'ForeignKey':
      query += str(getattr(objAttr, 'type_val')) + ' ' 
      query += 'REFERENCES '
      query += str(getattr(objAttr, 'pointer_to'))

    # FInd attributes for each field
    fieldAttrs = [attr for attr in dir(objAttr) if not callable(attr) and not attr.startswith("__")]
    print 'fieldAttrs ', fieldAttrs

    # Need to do size attribute first in the query
    if 'size' in fieldAttrs and objAttr.__class__.__name__ == 'CharField': 
      query += str(getattr(objAttr, 'size'))+') '

    
    # Add extra information about special field attributes
    for fieldAttrString in fieldAttrs:
      fieldAttr = getattr(objAttr, fieldAttrString)
      print 'fieldAttr ', fieldAttr
      if fieldAttrString == 'primary_key' and fieldAttr == True: 
        query += 'SERIAL PRIMARY KEY'
      elif fieldAttrString == 'not_null' and fieldAttr == True:
        query += 'NOT NULL'
      elif fieldAttrString == 'unique' and fieldAttr == True:
        query += 'UNIQUE'

    if classAttrs.index(attrString) != len(classAttrs)-1:
      query += ', '  

  query += '); '


print 'and the final result is the following query: ', query
