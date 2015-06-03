#!/bin/bash

apt-get update

apt-get -y install postgresql-contrib \
                   postgresql-server-dev-all \
                   python-dev python-pip \
                   thrift-compiler

mkdir /user_data
pip install virtualenv
virtualenv venv
cd /datahub
pip install -r requirements.txt
source src/setup.sh
python src/manage.py syncdb
python src/manage.py migrate inventory

python src/manage.py runserver 0.0.0.0:80
