#!/bin/bash

# Make sure the app container (www-data) and db container (postgres) are able
# to create and delete files and directories in the shared data volume
# (/user_data).
gosu root chown -R www-data:www-data /user_data/
gosu root chmod -R 3775 /user_data/
gosu root setfacl -d -R -m g:www-data:rwx /user_data
gosu root setfacl -d -R -m g:postgres:rwx /user_data
