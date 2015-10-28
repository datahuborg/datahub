#!/bin/bash

echo "Creating Docker containers..."
echo "(1/5) Creating \"logs\" - Data container for all server logs"
docker create --name logs \
    -v /var/log/postgresql \
    -v /var/log/gunicorn \
    -v /var/log/nginx \
    --entrypoint /bin/true \
    datahuborg/postgres
echo "(2/5) Creating \"data\" - Data container for Postgres db and user_data uploads"
docker create --name data \
    --entrypoint /bin/true \
    datahuborg/postgres
echo "(3/5) Creating \"db\" - Postgres server"
docker create --name db \
    --volumes-from data \
    --volumes-from logs \
    datahuborg/postgres
echo "(4/5) Creating \"app\" - gunicorn server hosting DataHub"
docker create --name app \
    --volumes-from data \
    --volumes-from logs \
    --link db:db \
    datahuborg/datahub gunicorn --config=provisions/gunicorn/config.py browser.wsgi
echo "(5/5) Creating \"web\" - nginx http proxy"
docker create --name web \
    --volumes-from app \
    --volumes-from logs \
    -v /ssl/:/etc/nginx/ssl/ \
    --link app:app \
    -p 80:80 -p 443:443 \
    datahuborg/nginx
echo "Done."