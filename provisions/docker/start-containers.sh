#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

echo "Starting containers..."
docker start db
echo "Waiting 5 seconds for db to spin up..."
sleep 5
# Make sure the database is up to date (should move this to a docker entrypoint script)
echo "Running Django migrations..."
docker run \
    --rm \
    --env 'USER=vagrant' \
    --volumes-from app \
    --net=datahub_dev \
    datahuborg/datahub \
    /bin/bash -c "python src/manage.py migrate --noinput"
docker start app
docker start web
echo "Done."
