#!/bin/bash

cd /datahub/src
set -x
python manage.py test integration_tests
