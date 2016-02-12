#!/bin/bash

cd /datahub/src
set -x
python manage.py test inventory
python manage.py test www
python manage.py test account
python manage.py test browser
python manage.py test core
python manage.py test api
