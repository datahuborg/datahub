#!/bin/bash

cd /datahub/src
set -x
python manage.py test inventory www account browser core api
