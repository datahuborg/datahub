import re
import json
import parser
import difflib
from collections import defaultdict

'''
@author: anant bhardwaj
@date: May 6, 2014

the goal is to infer a mapping function from a given list
of <un-structured text, structured fields> pairs
'''

def learn_mapping(training_input, training_output):
  i_data = json.loads(training_input)
  o_data = json.loads(training_output)
  o_fields_structure, i_structure = learn_structure(i_data, o_data)
  return o_fields_structure, i_structure

def learn_structure(i_data, o_data):
  i_chunks_list = []
  o_chunks_list = []
  for i in range(len(i_data)):
    i_chunks = parser.parse(i_data[i])
    i_chunks_list.append(i_chunks)
    o_chunks = [parser.parse(field) for field in o_data[i]]
    o_chunks_list.append(o_chunks)

  o_fields_structure = analyze_structure(o_chunks_list)
  i_structure = infer_input_structure(i_chunks_list, o_fields_structure)
  return o_fields_structure, i_structure

def analyze_structure(o_chunks_list):
  o_fields_structure = defaultdict(list)

  for o_chunks in o_chunks_list:
    for i in range(len(o_chunks)):
      o_fields_chunks = o_chunks[i]
      match_index = search_structure(o_fields_structure[i], o_fields_chunks)
      if(match_index != -1):
        o_fields_structure[i][match_index]['count'] += 1
      else:
        o_fields_structure[i].append({'field': i, 'type': o_fields_chunks, 'count': 1})

  return o_fields_structure


def search_structure(fields_structure, field_chunks):
  for i in range(len(fields_structure)):
    if match_type(fields_structure[i]['type'], field_chunks):
      return i

  return -1


def match_type(types_a, types_b):
  if len(types_a) != len(types_b):
    return False

  for i in range(len(types_a)):
    if types_a[i][0] != types_b[i][0]:
      return False

    if types_a[i][0] == 'OP':
      if types_a[i][1] != types_b[i][1]:
        return False

  return True


def infer_input_structure(i_chunks_list, o_fields_structure):
  i_fields_structure = defaultdict(list)
  for i_chunks in i_chunks_list:
    fields = analyze_input_structure(i_chunks, o_fields_structure)

def analyze_input_structure(i_chunks, o_fields_structure):
  i_chunks_types = [chunk[0] for chunk in i_chunks]
  extracted_fields = {}
  o_fields_types = []
  field_matches = defaultdict(list)
  for i in range(len(o_fields_structure)):
     for o_field_type in o_fields_structure[i][0]['type']:
      if o_field_type[0] == 'ENDMARKER':
        o_fields_types.append('ENDMARKER_%s' %(i))
      else:
        o_fields_types.append(o_field_type[0])
  
  matcher = difflib.SequenceMatcher(None, o_fields_types, i_chunks_types)
  alignments = matcher.get_opcodes()

  k = 0
  for i in range(len(o_fields_structure)):
    extracted_fields[i] = ''
    for alignment in alignments:
      if alignment[0] == 'equal' and alignment[1] >= k and (
          alignment[2] - alignment[1]) == len(o_fields_structure[i][0]['type']) - 1:      
        for k in range(alignment[3], alignment[4]):
          extracted_fields[i] += i_chunks[k][1]

        k = alignment[2]
        break

def extract(data, o_fields_structure, sep="\n"):
  o_data = data.split(sep)
  out = []
  for line in o_data:
    o_chunks = parser.parse(line)
    print line, o_chunks
    fields = extract_fields(o_chunks, o_fields_structure)
    out.append(fields)
  return out

def extract_fields(o_chunks, o_fields_structure):
  extracted_fields = {}
  o_chunks_types = [chunk[0] for chunk in o_chunks]
  o_fields_types = []
  field_matches = defaultdict(list)
  for i in range(len(o_fields_structure)):
     for o_field_type in o_fields_structure[i][0]['type']:
      if o_field_type[0] == 'ENDMARKER':
        o_fields_types.append('ENDMARKER_%s' %(i))
      else:
        o_fields_types.append(o_field_type[0])
  
  matcher = difflib.SequenceMatcher(None, o_fields_types, o_chunks_types)
  alignments = matcher.get_opcodes()

  k = 0
  for i in range(len(o_fields_structure)):
    extracted_fields[i] = ''
    for alignment in alignments:
      if alignment[0] == 'equal' and alignment[1] >= k and (
          alignment[2] - alignment[1]) == len(o_fields_structure[i][0]['type']) - 1:      
        for k in range(alignment[3], alignment[4]):
          extracted_fields[i] += o_chunks[k][1]
        k = alignment[2]
        break

  return extracted_fields
