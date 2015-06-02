FROM ubuntu:latest
MAINTAINER Denis Babani <dns.server@gmail.com>

VOLUME .:/datahub

RUN apt-get update

RUN apt-get -y install postgresql \
                   postgresql-contrib \
                   postgresql-server-dev-all \
                   python-dev python-pip \
                   thrift-compiler

RUN service postgresql start


RUN mkdir /user_data
RUN pip install virtualenv

RUN virtualenv venv

RUN sudo -u postgres createdb datahub
RUN sudo -u postgres psql -U postgres -d postgres -c "alter user postgres with password 'postgres';"

WORKDIR /datahub
RUN pip install -r requirements.txt

RUN source src/setup.sh
RUN python src/manage.py syncdb
RUN python src/manage.py migrate inventory
RUN source src/setup.sh

EXPOSE 80 80
RUN python src/manage.py runserver 0.0.0.0:80
