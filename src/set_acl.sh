#!/bin/sh
mkdir /user_data
chown -R postgres:www-data /user_data/
chmod -R 3775 /user_data/
setfacl -d -m g:www-data:rwx /user_data
setfacl -d -m g:postgres:rwx /user_data