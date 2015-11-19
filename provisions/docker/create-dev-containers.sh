#!/bin/bash

# Put your own certificate and private key at /ssl/nginx.crt and /ssl/nginx.key
# respectively on the host to have them picked up by the nginx container.

# The order of `--volumes-from` is important. The last one wins.
#
# `logs`, `data`, `db` are all based on the same image, so they have
# conflicting `VOLUME` declarations.
# - The standard postgres image declares the volume `/var/lib/postgresql/data`.
# - datahuborg/postgres inherits that and adds the volume `/user_data`.
# - The `logs` container below adds volumes for three log directories.
#
# When `db` includes volumes from `logs`, all five of those paths are overlaid
# in place of `db`'s content. Adding `data` last then overlays its content for
# the original two paths.
#
# This is necessary because only the postgres image has a postgres user with a
# logs directory that the user can write to, and the volume to the postgres
# data path is declared in the base postgres image, so having one requires the
# other.

echo "Creating Docker containers..."
echo "(1/6) Creating \"logs\" - Data container for all server logs"
docker create --name logs \
    -v /var/log/postgresql \
    -v /var/log/gunicorn \
    -v /var/log/nginx \
    --entrypoint /bin/true \
    datahuborg/postgres
echo "(2/6) Creating \"data\" - Data container for Postgres db and user_data uploads"
docker create --name data \
    --entrypoint /bin/true \
    datahuborg/postgres
echo "(3/6) Creating \"db\" - Postgres server"
docker create --name db \
    --volumes-from logs \
    --volumes-from data \
    datahuborg/postgres
echo "(4/6) Creating \"app\" - gunicorn server hosting DataHub"
docker create --name app \
    --volumes-from logs \
    --volumes-from data \
    --link db:db \
    -v /vagrant:/datahub \
    datahuborg/datahub gunicorn --config=provisions/gunicorn/config_dev.py browser.wsgi
echo "(5/6) Creating \"web\" - nginx http proxy"
docker create --name web \
    --volumes-from logs \
    --volumes-from app \
    -v /ssl/:/etc/nginx/ssl/ \
    --link app:app \
    -p 80:80 -p 443:443 \
    datahuborg/nginx
echo "(6/6) Creating \"test browser\" - phantomjs"
docker create --name phantomjs \
    wernight/phantomjs
echo "Done."
