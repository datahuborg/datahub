"""
@author: Jesika Haria
@date: Oct 30, 2013

DataHub ORM Fields (Python)
"""

#TODO: Make the inheritance and changing attribute work 
# TODO: Add more fields if needed, more options such as:
# primary_key, foreign_key, not null, unique, default, check (?)

class BaseModel():
  def __init__(self):
    pass

'''Base class for fields'''
class Field(object):
  max_length = 50
  def __init__(self, **kwargs):
    self.primary_key = False
    # Not sure whether to leave this in or not 
    super(Field, self).__init__()


''' varchar(size)'''
class CharField(Field):
  def __init__(self, **kwargs):
    self.size = kwargs.pop('size',30)
    super(CharField, self).__init__(**kwargs)


''' int '''
class IntegerField(Field):
  def __init__(self, **kwargs):
    super(IntegerField, self).__init__(**kwargs)


''' boolean '''
class BooleanField(Field):
  def __init__(self, **kwargs):
    super(BooleanField, self).__init__(**kwargs)


''' datetime '''
class DatetimeField(Field):
  def __init__(self, **kwargs):
    super(DatetimeField, self).__init__(**kwargs)


''' timestamp '''
class TimestampField(Field):
  def __init__(self, **kwargs):
    super(TimestampField, self).__init__(**kwargs)
