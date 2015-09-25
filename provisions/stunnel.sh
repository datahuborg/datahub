#!/bin/bash

dpkg -s stunnel4 > /dev/null
if [ $? -ne 0 ]
then
  apt-get update

  apt-get -y install stunnel4
fi


cd /datahub

rm stunnel/datahub.conf
echo "pid=

cert = stunnel/stunnel.pem
foreground = yes
output = stunnel.log

[https]
accept=443
connect=${DATAHUB_PORT_80_TCP_ADDR}:80
TIMEOUTclose=1" > stunnel/datahub.conf

stunnel4 stunnel/datahub.conf
