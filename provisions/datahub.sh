#!/bin/bash

dpkg -s thrift-compiler > /dev/null
if [ $? -ne 0 ]
then
  apt-get update

  apt-get -y install postgresql-contrib \
                     postgresql-server-dev-all \
                     python-dev python-pip \
                     thrift-compiler

  export PGPASSWORD=postgres
  export PGUSER=postgres
  createdb -h db -p 5432 -U postgres datahub

  mkdir /user_data

  pip install virtualenv
  virtualenv venv
fi


cd /datahub
pip install -r requirements.txt
source src/setup.sh
python src/manage.py syncdb
python src/manage.py migrate inventory

cd /datahub

python src/manage.py runserver 0.0.0.0:80
