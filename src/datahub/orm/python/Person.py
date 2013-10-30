import models
# will be import datahub.models and super class will be models.BaseModel

class Person(models.BaseModel):
  first_name = models.CharField(size=30)
  #last_name = models.CharField(size=30)


