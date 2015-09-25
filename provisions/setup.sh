#!/bin/bash
apt-get update

apt-get -y install wget postgresql-client-common postgresql-client
wget -qO- https://get.docker.com/ | sh

export PGPASSWORD=postgres
export PGUSER=postgres

# create database container
docker run --name db  -v /user_data:/user_data:ro -e POSTGRES_PASSWORD=$PGPASSWORD -e POSTGRES_USER=$PGUSER -p 5432:5432 -d postgres
export DBIP=`docker inspect -f '{{ .NetworkSettings.IPAddress }}' db`

# create datahub container
docker run --name datahub -d -v /vagrant:/datahub -v /user_data:/user_data --link db:db -p 80:80 ubuntu /bin/bash -C "/datahub/provisions/datahub.sh"

export DATAHUBIP=`docker inspect -f '{{ .NetworkSettings.IPAddress }}' datahub`

# create SSH tunnel to give an HTTPS path to datahub
docker run --name stunnel -d -v /vagrant:/datahub --link datahub:datahub -p 443:443 ubuntu /bin/bash -C "/datahub/provisions/stunnel.sh"


echo "
#!/bin/bash

docker stop stunnel
docker stop datahub
docker stop db
" > /etc/rc6.d/K99_stop_docker

chmod +x /etc/rc6.d/K99_stop_docker

echo "
#!/bin/bash

docker start db
docker start datahub
docker start stunnel
" > /etc/init.d/start_dockers

chmod +x /etc/init.d/start_dockers

ln -s /etc/init.d/start_dockers /etc/rc2.d/S99start_dockers

echo "Database IP: $DBIP"
echo "Datahub  IP: $DATAHUBIP"
