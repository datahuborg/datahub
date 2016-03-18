import json
import ast

from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.finders import find
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from distill import inference
from serializer import DistillationSerializer


'''
@author: Anant Bhardwaj
@date: Mar 21, 2013

Datahub Refiner
'''

# working JSON when input through django-rest-api
# https://datahub-local.mit.edu/apps/refiner/api/v1/refiner
# {
# "training_input": ["2012-01-04 00:01:23,180 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Receiving block blk_-2281137920769708011_1116 src: /127.0.0.1:32981 dest: /127.0.0.1:50010",
# "2012-01-04 00:01:23,185 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: PacketResponder 0 for block blk_-2281137920769708011_1116 terminating"]
# ,
# "training_output": [
# ["2012-01-04", "00:01:23", "127.0.0.1:32981", "127.0.0.1:50010"],
# ["2012-01-04", "00:01:23", "", ""]
# ]
# ,
# "test_data": "2012-01-04 00:01:23,180 INFO org.apache.hadoop.hdfs.server.datanode.DataNode: Receiving block blk_-2281137920769708011_1116 src: \/127.0.0.1:32981 dest: \/127.0.0.1:50010\r\n2012-01-04 00:01:23,184 INFO org.apache.hadoop.hdfs.server.datanode.DataNode.clienttrace: src: \/127.0.0.1:32981, dest: \/127.0.0.1:50010, bytes: 3758, op: HDFS_WRITE, cliID: DFSClient_-603743753, offset: 0, srvID: DS-292194659-127.0.1.1-50010-1324763300176, blockid: blk_-2281137920769708011_1116, duration: 2016056\r\n"
# }


@login_required
def index(request):

    # load data from static files and pass it to the view
    crime_training_input = file(find('crime/input.txt')).read()
    crime_training_output = file(find('crime/output.txt')).read()
    crime_test = file(find('crime/test.txt')).read()

    hadoop_training_input = file(find('hadoop/input.txt')).read()
    hadoop_training_output = file(find('hadoop/output.txt')).read()
    hadoop_test = file(find('hadoop/test.txt')).read()

    return render_to_response("refiner.html", {
        'login': request.user.get_username(),
        'crime_training_input': crime_training_input,
        'crime_training_output': crime_training_output,
        'crime_test': crime_test,
        'hadoop_training_input': hadoop_training_input,
        'hadoop_training_output': hadoop_training_output,
        'hadoop_test': hadoop_test,
    })


class Refiner(APIView):
    """
    Structures semi-structured data
    """

    def post(self, request):
        """
        Generate a CSV from semi-strutured text
        ---
        parameters:
        - name: training_input
          in: body
          type: string
          description: example data that is in the file
          required: true
        - name: training_output
          in: body
          type: string
          description:
            what you would like the data to look like after processing
          required: true
        - name: test_data
          in: body
          type: string
          description: the data to be processed
          required: false
        - name: record_separator
          in: body
          type: string
          description:
            separator of different records. \\n is used by default
          required: false
        - name: test_data_file
          type: file
          description: text file containing data to be parsed
        """

        data = request.data
        training_input = data['training_input']
        training_output = data['training_output']
        record_separator = data.get('record_separator', '\n')



        distillation = inference.Distillation(
            training_input, training_output, record_separator, test_data, test_data_file)
        serializer = DistillationSerializer(distillation)
        return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
def refine_data(request):
    res = {'error': None}

    if request.method == 'POST':
        try:
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
        except Exception, e:
            res['error'] = str(e)
    else:
        res['error'] = 'Invalid HTTP Method'

    return HttpResponse(json.dumps(res), content_type="application/json")
