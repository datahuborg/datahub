#!/bin/bash

echo "Starting containers..."
docker start db
echo "Waiting 5 seconds for db to spin up..."
sleep 5
# Make sure the database is up to date (should move this to a docker entrypoint script)
echo "Running Django migrations..."
docker run --rm --link db:db --volumes-from app datahuborg/datahub python src/manage.py migrate
docker start app
docker start web
echo "Done."
