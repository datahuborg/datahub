#!/bin/bash

echo "Starting containers..."
docker start db
sleep 5
# Make sure the database is up to date (should move this to a docker entrypoint script)
docker run --rm --link db:db datahuborg/datahub python src/manage.py migrate
docker start app
docker start web
echo "Done."