import json
import os
import sys

from collections import OrderedDict


'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub Model Parser
'''

def parse(in_file, write_to_file=False):
  in_f = open(in_file).read()
  data = json.loads(in_f, object_pairs_hook=OrderedDict)
  out = ''

  for t in data:
    i = 1
    out += "struct %s {\n" % (t['model'])
    for field in t['fields']:
      out += "  %d: optional %s %s,\n" % (i , t['fields'][field]['type'], field)
      i += 1

    out += "}\n"
    out += "\n"
  
  if write_to_file:
    out_f = open(os.path.splitext(in_file)[0] + '.thrift', 'w+')
    out_f.write(out)
    out_f.close()

  return out

  

def test():
  print parse(sys.argv[1], write_to_file=True)

if __name__ == '__main__':
  test()