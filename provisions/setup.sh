#!/bin/bash
apt-get update

apt-get -y install wget postgresql-client-common postgresql-client
wget -qO- https://get.docker.com/ | sh

export PGPASSWORD=postgres
export PGUSER=postgres


# create database container
docker run --name db -e POSTGRES_PASSWORD=$PGPASSWORD -e POSTGRES_USER=$PGUSER -d postgres
export DBIP=`docker inspect -f '{{ .NetworkSettings.IPAddress }}' db`
createdb -h $DBIP -p 5432 -U postgres datahub

# create datahub container
docker run --name datahub -d -v /vagrant:/datahub --link db:db -p 80:80 ubuntu /bin/bash -C "/datahub/provisions/datahub.sh"

export DATAHUBIP=`docker inspect -f '{{ .NetworkSettings.IPAddress }}' datahub`

echo $DATAHUBIP

# echo "map \$http_host \$container {
#   default \"$DATAHUBIP:80\";
# }
# server {
#   listen 80;
#   location / {
#     proxy_pass  http://\$container;
#     proxy_http_version  1.1;
#     proxy_set_header  Connection        \"\";
#     proxy_set_header  Host              \$host;
#     proxy_set_header  X-Real-IP         \$remote_addr;
#     proxy_set_header  X-Forwarded-For   \$proxy_add_x_forwarded_for;
#   }
# }
# " > /etc/nginx/sites-enabled/default


# in the container
# apt-get -y install postgresql \
#                    postgresql-contrib \
#                    postgresql-server-dev-all \
#                    python-dev python-pip \
#                    thrift-compiler
#
# service postgresql start
#
# sudo -u postgres createdb datahub
# sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"
#
#
# mkdir /user_data
#
# cd /vagrant
# pip install virtualenv
#
# virtualenv venv
# pip install -r requirements.txt
#
# source src/setup.sh
# python src/manage.py syncdb
# python src/manage.py migrate inventory
#
#
# wget -qO- https://get.docker.com/ | sh
#
# b9b0daa57b2c
