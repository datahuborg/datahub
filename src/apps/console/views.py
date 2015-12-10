from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Console
'''


@login_required
def index(request):
    return render_to_response("console.html", {
        'login': request.user.username})
