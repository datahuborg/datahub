from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Viz
'''


@login_required
def index(request):
    login = request.user.get_username()
    return render_to_response("viz.html", {
        'login': login,
        'repo_base': login
    })
