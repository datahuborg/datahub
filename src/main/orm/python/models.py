"""
@author: Jesika Haria
@date: Oct 30, 2013

DataHub ORM Fields (Python)
"""

# TODO: Add more fields if needed, more options such as:
# primary_key, foreign_key, not null, unique, default, check (?)

class BaseModel():
  def __init__(self):
    pass

'''Base class for fields'''
class Field(object):
  def __init__(self, **kwargs):
    self.size = 50
    self.primary_key = False
    self.not_null = False
    self.unique = False

    super(Field, self).__init__()


''' varchar(size)'''
class CharField(Field):
  def __init__(self, **kwargs):
    super(CharField, self).__init__(**kwargs)
    
    self.size = kwargs.pop('size', 30)
    self.primary_key = kwargs.pop('primary_key', False)
    self.not_null = kwargs.pop('not_null', False)
    self.unique = kwargs.pop('unique', False)

''' int '''
class IntegerField(Field):
  def __init__(self, **kwargs):
    super(IntegerField, self).__init__(**kwargs) 
    self.primary_key = kwargs.pop('primary_key', False)
    self.not_null = kwargs.pop('not_null', False)
    self.unique = kwargs.pop('unique', False)


''' boolean '''
class BooleanField(Field):
  def __init__(self, **kwargs):
    super(BooleanField, self).__init__(**kwargs)
    self.primary_key = kwargs.pop('primary_key', False)
    self.not_null = kwargs.pop('not_null', False)
    self.unique = kwargs.pop('unique', False)


''' datetime '''
class DatetimeField(Field):
  def __init__(self, **kwargs):
    super(DatetimeField, self).__init__(**kwargs)
    self.primary_key = kwargs.pop('primary_key', False)
    self.not_null = kwargs.pop('not_null', False)
    self.unique = kwargs.pop('unique', False)


''' timestamp '''
class TimestampField(Field):
  def __init__(self, **kwargs):
    super(TimestampField, self).__init__(**kwargs)
    self.primary_key = kwargs.pop('primary_key', False)
    self.not_null = kwargs.pop('not_null', False)
    self.unique = kwargs.pop('unique', False)


'''foreign key'''
class ForeignKey():
  def __init__(self, pointer_to, type_val='integer'):
    self.pointer_to = pointer_to
    self.type_val = type_val


'''testing'''
if __name__ == '__main__':
  f = Field()
  print f.primary_key

  c = CharField(primary_key=True)
  print c.primary_key

  i = IntegerField()
  i.primary_key = True 
