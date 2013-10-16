#!/usr/bin/python
import os
import sys
sys.path.append(
    os.path.dirname(os.path.abspath(__file__)) + '/gen-py'
  )

from model.constants import *

'''
@author: anant bhardwaj
@date: Oct 11, 2013

Sample python code accesing DataHub APIs
'''

sam = Faculty (id=1, name='Sam Madden')
david = Faculty (id=2, name='David Karger')

db = Course (id=1, name='Database Systems', faculty=sam)
algo = Course (id=2, name='Advance Algorithms', faculty=david)

print db