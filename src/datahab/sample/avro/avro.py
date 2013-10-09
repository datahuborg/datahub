import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter

'''
@author: anant bhardwaj
@date: Oct 9, 2013

Avro Sample Code
'''

schema = avro.schema.parse(open("sample.avsc").read())


writer = DataFileWriter(open("data.avro", "w"), DatumWriter(), schema)
csail = {"id":1, "name": "MIT Computer Science & Artificial Intelligence Lab"}
writer.append({"id": 1, "name": "Sam Madden", "dept": csail, "sex": "Male"})
writer.append({"id": 2, "name": "David Karger", "dept": csail, "sex": "Male"})
writer.close()

reader = DataFileReader(open("data.avro", "r"), DatumReader())
for user in reader:
    print user
reader.close()