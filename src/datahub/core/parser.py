import json
import os
import sys
import subprocess

from collections import OrderedDict


'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub Model Parser
'''

allowed_type = [
    'boolean',
    'smallint',
    'integer',
    'bigint',
    'double',
    'text',
    'varchar',
    'binary',
    'date',
    'time',
    'timestamp',
    'foreign_key'
  ]

thrift_map = {
    'boolean': 'bool',
    'smallint': 'i16',
    'integer': 'i32',
    'bigint': 'i64',
    'double': 'double',
    'text': 'string',
    'varchar': 'string',
    'binary': 'binary',
    'date': 'string',
    'time': 'string',
    'timestamp': 'bigint',
  }

sql_map = {
    'boolean': 'boolean',
    'smallint': 'smallint',
    'integer': 'integer',
    'bigint': 'bigint',
    'double': 'double',
    'text': 'text',
    'varchar': 'varchar',
    'binary': 'bytea',
    'date': 'date',
    'time': 'time',
    'timestamp': 'timestamp',
  }


def parse(in_file, write_to_file=False):
  in_f = open(in_file).read()
  data = json.loads(in_f, object_pairs_hook=OrderedDict)
  thrift_out = ''
  sql_out = ''
  table_map = {}

  for t in data:
    table = t['model']
    i = 1
    table_map[table] = {}
    thrift_out += "struct %s {\n" % (table)
    sql_out += "CREATE TABLE %s (" % (table)
    num_fields = len(t['fields'])

    for field in t['fields']:
      field_type = t['fields'][field]['type']
      if field_type not in allowed_type:
        raise Exception('wrong type: %s' %(t['fields'][field]['type']))

      if field not in table_map[table]:
        table_map[table][field] = {}

      table_map[table][field].update({'type': t['fields'][field]['type']})

      if (field_type == 'foreign_key'):
        foreign_table = t['fields'][field]['table']
        foreign_field = t['fields'][field]['field']
        thrift_out += "  %d: optional %s %s" % (
            i ,
            t['fields'][field]['table'],
            field
          )
        sql_out += "%s %s references %s(%s)" % (
            field,
            table_map[foreign_table][foreign_field]['type'],
            foreign_table,
            foreign_field
          )
      else:
        thrift_out += "  %d: optional %s %s" % (i , thrift_map[field_type], field)
        sql_out += "%s %s" % (field, sql_map[field_type])

      if i < num_fields:
        thrift_out += ",\n"
        sql_out += ", "

      i += 1        

    thrift_out += "\n}\n\n"
    sql_out += ");\n"
  
  if write_to_file:
    out_f_name = os.path.abspath(os.path.splitext(in_file)[0] + '.thrift')
    out_f = open(out_f_name, 'w+')
    out_f.write(thrift_out)
    out_f.close()

    cmd = ["thrift --gen py -o %s %s" % (
        os.path.dirname(out_f_name), out_f_name)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell = True)
    out, err = p.communicate()

  return thrift_out, sql_out
  

def test():
  thrift_out, sql_out = parse(sys.argv[1], write_to_file=True)
  print thrift_out
  print sql_out

if __name__ == '__main__':
  test()