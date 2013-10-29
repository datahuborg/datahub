from django.db import models

'''
Datahub Models

@author: Anant Bhardwaj
@date: Mar 21, 2013
'''
class Type:
	Boolean=1
	Char=2

class Value:
	val = None

class Field()
	Type type
	Value val
	bool is_pr
	bol is_au
	int max_len

class IntegerField(Field):
	def __init__():
		super.primary_key = True



class Model:
	Filed f = []




class User(models.Model):
	id = models.AutoField(primary_key=True)
	email = models.CharField(max_length=100, unique = True)
	username = models.CharField(max_length=50, unique = True)
	password = models.CharField(max_length=50)
	active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "users"


class Database(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, unique = True)
	owner = models.ForeignKey('User')
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "databases"


class Table(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	schema = models.TextField()
	version = models.IntegerField()
	database = models.ForeignKey('Database')
	timestamp = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

	class Meta:
		db_table = "tables"




