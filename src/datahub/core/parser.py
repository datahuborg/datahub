import json
import os
import sys

from collections import OrderedDict


'''
@author: anant bhardwaj
@date: Oct 3, 2013

DataHub Model Parser
'''

def parse(in_file):
  in_f = open(in_file).read()
  data = json.loads(in_f, object_pairs_hook=OrderedDict)
  out = ''

  for t in data.keys():
    i = 1
    out += "struct %s {\n" % (t)
    for f in data[t].keys():
      out += "  %d: optional %s %s,\n" % (i , data[t][f]['type'], f)
      i += 1

    out += "}\n"
    out += "\n"
  
  out_f = open(os.path.splitext(in_file)[0] + '.thrift', 'w+')
  out_f.write(out)
  out_f.close()

  return out

  

def test():
  print parse(sys.argv[1])

if __name__ == '__main__':
  test()