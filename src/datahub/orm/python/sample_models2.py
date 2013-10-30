import models

class Animal(object):
  species = models.CharField(size=30,primary_key=True)
  life_expectancy = models.IntegerField()
