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
  f_name = models.CharField(max_length=50, null=True)
  l_name = models.CharField(max_length=50, null=True)
  password = models.CharField(max_length=50)
  active = models.BooleanField(default=False)
  
  def __unicode__(self):
    return self.username

  class Meta:
    db_table = "users"


class View(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  url_path = models.CharField (max_length=200, unique = True)
  repo_base = models.CharField(max_length=50)
  repo_name = models.CharField(max_length=50)
  view_name = models.CharField (max_length=50)

  def __unicode__(self):
    return self.url_path

  class Meta:
    db_table = "views"


class Annotation(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  url_path = models.CharField (max_length=500, unique = True)
  url_blurb = models.TextField ()

  def __unicode__(self):
    return self.id

  class Meta:
    db_table = "annotations"


class Comments(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  url_path = models.CharField (max_length=500)
  comment = models.TextField ()

  def __unicode__(self):
    return self.id

  class Meta:
    db_table = "comments"

class App(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  app_id = models.CharField (max_length=100, unique = True)
  app_name = models.CharField (max_length=100)
  app_token = models.CharField (max_length=500)
  user = models.ForeignKey ('User')

  def __unicode__(self):
    return self.app_name

  class Meta:
    db_table = "apps"


class Permission(models.Model):
  id = models.AutoField(primary_key=True)
  timestamp = models.DateTimeField(auto_now=True)
  user = models.ForeignKey('User')
  app = models.ForeignKey('App')
  access = models.BooleanField(default=False)

  def __unicode__(self):
    return self.id

  class Meta:
    db_table = "permissions"