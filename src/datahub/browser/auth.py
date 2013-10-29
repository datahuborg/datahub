import json, sys, re, hashlib, smtplib, base64, urllib, os

from django.http import *
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.validators import email_re
from django.db.utils import IntegrityError
from django.utils.http import urlquote_plus
from schema.models import *
from browser.utils import *


'''
@author: Anant Bhardwaj
@date: Feb 12, 2012
'''

kLogIn = "SESSION_LOGIN"
kName = "SESSION_NAME"


def is_valid_username (username):
  try:
    if len(username) >3 and re.match(r'\w+', username).group() == username:
      return True
  except:
    pass

  return False

def login_required (f):
    def wrap (request, *args, **kwargs):
        if kLogIn not in request.session.keys():
        	if(len(args)>0):
        		redirect_url = urlquote_plus("/%s/%s" %(args[0], f.__name__))
        	else:
        		redirect_url = "/"
        	return HttpResponseRedirect("/login?redirect_url=%s" %(redirect_url))
        return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def login_form (request, redirect_url='/', errors=[]):
    c = {'redirect_url':redirect_url, 'errors':errors}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def register_form (request, redirect_url='/', errors=[]):
    c = {'redirect_url':redirect_url, 'errors':errors}
    c.update(csrf(request))
    return render_to_response('register.html', c)


def login (request):
    redirect_url = '/'
    if('redirect_url' in request.GET.keys()):
    	redirect_url = request.GET['redirect_url']

    if not redirect_url or redirect_url == '':
      redirect_url = '/'

    if request.method == "POST":
    	errors = []
    	if('redirect_url' in request.POST.keys()):
    		redirect_url = request.POST['redirect_url']
        email = None
        try:
            login_id = request.POST["login_id"].lower()
            login_password = hashlib.sha1(request.POST["login_password"]).hexdigest()
            email = email_re.match(login_id.lower().strip())
            user = None
            if email:
              user = User.objects.get(email=login_id, password=login_password)
            else:
              user = User.objects.get(username=login_id, password=login_password)

            request.session.flush()
            request.session[kLogIn] = user.username
            return HttpResponseRedirect(redirect_url)
        except User.DoesNotExist:
          try:
            if email:
              User.objects.get(email=login_id)
            else:
              User.objects.get(username=login_id)
            errors.append('Wrong password.')
          except User.DoesNotExist:
            errors.append("Couldn't locate account with login id: %s" %(login_id))
          return login_form(request, redirect_url = redirect_url, errors = errors) 
        except:
            errors.append('Login failed.')
            return login_form(request, redirect_url = redirect_url, errors = errors)          
    else:
        return login_form(request, redirect_url)

def register (request):
    redirect_url = '/'
    if('redirect_url' in request.GET.keys()):
    	redirect_url = request.GET['redirect_url']
    if request.method == "POST":
    	errors = []
        try:
            error = False
            if('redirect_url' in request.POST.keys()):
              redirect_url = request.POST['redirect_url']
            username = request.POST["username"].lower()
            email = request.POST["email"].lower()
            password = request.POST["password"]
      
            if(email_re.match(email.strip()) == None):
            	errors.append("Invalid Email.")
            	error = True
            if(not is_valid_username(username)):
              errors.append("Invalid Username.")
              error = True
            if(password == ""):
            	errors.append("Empty Password.")
            	error = True

            try:
              user = User.objects.get(username=username)
              errors.append("Username already taken.")
              error = True
            except User.DoesNotExist:
              pass

            if(error):
            	return register_form(request, redirect_url = redirect_url, errors = errors)
            hashed_password = hashlib.sha1(password).hexdigest()
            user = User(username=username, email=email, password=hashed_password)
            user.save()
            request.session.flush()
            request.session[kLogIn] = user.username
            return HttpResponseRedirect(redirect_url)
        except IntegrityError:
            errors.append("Account with the email address %s already exists. Please Log In." %(email))
            return register_form(request, redirect_url = redirect_url, errors = errors)
        except Exception, e:
            errors.append(e.message)
            return register_form(request, redirect_url = redirect_url, errors = errors)
    else:
        return register_form(request, redirect_url = redirect_url)


def logout (request):
    request.session.flush()
    if kLogIn in request.session.keys():
    	del request.session[kLogIn]
    return HttpResponseRedirect('/')


def forgot (request):
  if request.method == "POST":
    errors = []
    try:
      login_id = request.POST["login_id"].lower()
      email = email_re.match(login_id.lower().strip())
      user = None
      if email:
        user = User.objects.get(email=login_id)
      else:
        user = User.objects.get(username=login_id)
      
      user_email = user.email
      decrypted_email = encrypt_text(user_email)

      subject = "DataHub Password Reset"

      msg_body = '''
      Dear %s,

      Please click the link below to reset your confer password:

      http://datahub.csail.mit.edu/reset/%s

      ''' % (user_email, decrypted_email)

      send_email(user_email, subject, msg_body)

      c = {
        'msg_title': 'DataHub Reset Password',
        'msg_body': 'A link to reset your password has been sent to your email address.'
      } 
      c.update(csrf(request))

      return render_to_response('confirmation.html', c)

    except User.DoesNotExist:
      errors.append(
          "Invalid Username / Email Address.")
    except Exception, e:
      errors.append(
          "Some unknown error happened: %s"
          "Please report it to datahub@csail.mit.edu." %(e.message))
    
    c = {'errors': errors} 
    c.update(csrf(request))
    return render_to_response('forgot.html', c)
  else:
    return render_to_response('forgot.html', csrf(request))


def reset (request, encrypted_email):
  errors = []
  error = False
  if request.method == "POST":
    try:
      user_email = request.POST["user_email"].lower()
      password = request.POST["new_password"]
      password2 = request.POST["new_password2"]

      if password == "":
        errors.append("Empty Password.")
        error = True

      if password2 != password:
        errors.append("Password and Confirm Password don't match.")
        error = True

      if error:
        c = {
          'user_email': user_email,
          'encrypted_email': encrypted_email,
          'errors': errors
        }
        c.update(csrf(request))
        return render_to_response('reset.html', c)

      else:
        hashed_password = hashlib.sha1(password).hexdigest()
        user = User.objects.get(email=user_email)
        user.password = hashed_password
        user.save()
        c = {
          'msg_title': 'DataHub Reset Password',
          'msg_body': 'Your password has been changed successfully.'
        } 
        c.update(csrf(request))
        return render_to_response('confirmation.html', c)
    except:
      errors.append(
          'Some unknown error happened. '
          'Please try again or send an email to '
          'datahub@csail.mit.edu.')
      c = {'errors': errors} 
      c.update(csrf(request))
      return render_to_response('reset.html', c)
  else:
    try:
      user_email = decrypt_text(encrypted_email)
      User.objects.get(email=user_email)
      c = {
          'user_email': user_email,
          'encrypted_email': encrypted_email
      }
      c.update(csrf(request))
      return render_to_response('reset.html', c)
    except:
      errors.append(
          'Wrong reset code in the URL. '
          'Please try again or send an email to '
          'confer@csail.mit.edu.')
    
    c = {'msg_title': 'DataHub Reset Password', 'errors': errors} 
    c.update(csrf(request))
    return render_to_response('confirmation.html', c)
