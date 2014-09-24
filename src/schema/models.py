from django.db import models

'''
Datahub Models

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''

class User(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.CharField(max_length=100, unique = True)
	username = models.CharField(max_length=50, unique = True)
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=50)
	active = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "users"




