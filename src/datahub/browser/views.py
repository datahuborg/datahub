import json, sys, re, hashlib, smtplib, base64, urllib, os

from auth import *
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
			db_names = [t[0] for t in res['tuples']]
			return render_to_response("user.html", {'username': username, 'db_names':db_names})
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
		res = manager.list_tables(username, db_name)
		table_names = [t[0] for t in res['tuples']]
		return render_to_response("database.html", {
				'username': username,
				'db_name':db_name,
				'table_names':table_names})
	except Exception, e:
		print str(e)
		return HttpResponse({'error': str(e)}, mimetype="application/json")

@login_required
def table(request, username, db_name, table_name):
	try:
		res = manager.load_table(username, db_name, table_name)
		column_names = res['column_names']
		tuples = res['tuples']
		return render_to_response("table.html", {
				'username': username,
				'db_name':db_name,
				'table_name':table_name,
				'column_names': column_names,
				'tuples': tuples})
	except Exception, e:
		return HttpResponse({'error': str(e)}, mimetype="application/json")



