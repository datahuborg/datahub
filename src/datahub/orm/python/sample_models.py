import models

class Person(object):
  first_name = models.CharField(size=30,primary_key=True)
  last_name = models.CharField(size=30)
  age = models.IntegerField()
  dob = models.DatetimeField()
  isMale = models.BooleanField()

class Faculty(object):
  first_name = models.CharField(size=35)
  last_name = models.CharField(size=35)
