import json, sys, re, hashlib, smtplib, base64, urllib, os

from auth import *
from core.db import account_manager as manager
from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus

'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Web Handler
'''

@login_required
def user(request, username=None):
	try:
		if(username):
			res = manager.list_databases(username)
			return render_to_response("user.html", {'username': username, 'db_names':res['db_names']})
		else:
			user = request.session[kUsername]
			return HttpResponseRedirect(user)
	except KeyError:
		return HttpResponseRedirect('/login')


def new_database_form(request, username):
	return render_to_response("new_database.html", {'username': username})

@login_required
def new_database(request, username, db_name):
	manager.create_database(username, db_name)
	return HttpResponseRedirect("/"+username)

@login_required
def database(request, username, db_name):
	try:
		res = manager.list_tables(db_name)
		return render_to_response("database.html", {'username': username, 'db_name':db_name, 'table_names':res['table_names']})
	except Exception, e:
		return HttpResponse(request_error, mimetype="application/json")

@login_required
def table(request, username, db_name, table_name):
	try:
		return render_to_response("table.html", {'username': username, 'db_name':db_name, 'table_name':table_name})
	except Exception, e:
		return HttpResponse(request_error, mimetype="application/json")



