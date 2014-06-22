import sys
import refiner.inference

'''
@author: anant bhardwaj
@date: May 6, 2014

a sample client code for automated-date cleaning
'''
crime_sep = "==========\n"
o_fields_structure, i_structure = refiner.inference.learn_mapping(open(sys.argv[1]).read(), open(sys.argv[2]).read())
print o_fields_structure
print i_structure

out = refiner.inference.extract(open(sys.argv[3]).read(), o_fields_structure)
for row in out:
  print '\t'.join(row.values())
