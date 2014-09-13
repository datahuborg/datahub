import models


'''
@author Jesika Haria
@date November 6, 2013

Sample Models for ORM Testing (Python)
'''
class Person(object):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(size=30)
  email = models.CharField(size=30, unique=True)
  age = models.IntegerField()
  dob = models.DatetimeField(not_null=True)
  isMale = models.BooleanField()
  project_id = models.ForeignKey('Project')


class Project(object):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(size=35)

'''
Sample operations
 
Object creation 
project1 = Project.new(name='First Project') 
person1 = Person.new(name='Jess', email='jesika@mit.edu', age=20, dob='1992/11/29', isMale=False, project_id=1)

Referencing object
project1 = Project.find(1) # if nothing specified, then assume it is an id
person1 = Person.find(name='Jess', isMale=False)

Updating object
person1.update(name='Jesika') 

Deleting object
person1.delete()

Saving changes # is this required? 
'''



