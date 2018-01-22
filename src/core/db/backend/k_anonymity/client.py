#!/usr/bin/python

"""
import kanonymizer
import argparse
import pgdb

parser = argparse.ArgumentParser()
parser.add_argument("--table")
parser.add_argument("--attributes", nargs="*")
parser.add_argument("-k", type=int)

args = parser.parse_args()

connection = pgdb.connect(host="localhost", database="testdb")
kanonymizer = kanonymizer.KAnonymizer(connection, args.table, args.attributes, args.k)
print kanonymizer.anonymize()
"""