#!/bin/bash
apt-get -y install postgresql \
                   postgresql-contrib \
                   postgresql-server-dev-all \
                   python-dev python-pip \
                   thrift-compiler
sudo -u postgres createdb datahub
sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"


mkdir /user_data

cd /vagrant
pip install virtualenv

virtualenv venv
pip install -r requirements.txt

source src/setup.sh
python src/manage.py syncdb
python src/manage.py migrate inventory
