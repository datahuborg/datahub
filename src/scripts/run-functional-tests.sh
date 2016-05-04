#!/bin/bash

cd /datahub/src
set -x
python manage.py test functional_tests.test_login_auth
python manage.py test functional_tests.test_layout_and_styling
python manage.py test functional_tests.test_db
python manage.py test functional_tests.test_api
python manage.py test functional_tests.test_console
