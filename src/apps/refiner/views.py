import json

from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from core.db.manager import DataHubManager
from distill import inference


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Refiner
'''


def index(request):
    res = {'login': request.user.get_username}
    res.update(csrf(request))
    return render_to_response("refiner.html", res)


def refine_data(request):
    res = {'error': None}
    try:
        if request.method == 'POST':
            training_input = request.POST['training_input']
            training_output = request.POST['training_output']
            test_data = request.POST['test_data']
            record_separator = '\n'
            if 'record_separator' in request.POST:
                record_separator = request.POST['record_separator']

            o_fields_structure, i_structure = inference.learn_mapping(
                training_input, training_output)
            out = inference.extract(
                test_data, o_fields_structure, sep=record_separator)

            csv_lines = []
            for row in out:
                csv_lines.append(','.join(row.values()))

            csv_str = '\n'.join(csv_lines)
            res['output'] = csv_str
            res['csv_lines'] = csv_lines
        else:
            res['error'] = 'Invalid HTTP Method'
    except Exception, e:
        res['error'] = str(e)

    return HttpResponse(json.dumps(res), content_type="application/json")


@login_required
def create_table(request):
    username = request.user.get_username
    csv_lines = request.POST.getlist('csv_lines[]')
    header = json.loads(request.POST['header'])
    repo = request.POST['repo_name']
    table = request.POST['table_name']

    # remove the "..." characters that refiner puts on both sides of the array
    csv_lines = csv_lines[1:len(csv_lines) - 1]
    with DataHubManager(username) as m:
        m.import_rows(
            repo=repo,
            table=table,
            rows=csv_lines,
            header=header)

    return True
