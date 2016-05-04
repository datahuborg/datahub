#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

echo "Starting phantomjs container..."
if ! `docker inspect -f {{.State.Running}} phantomjs`; then
    (set -x; docker start phantomjs)
    echo "phantomjs started."
else
    echo "phantomjs already running. Skipping."
fi
echo "Stopping app container..."
(set -x; docker stop app)
echo "Spinning up test app container..."
echo "*** Run unit tests with 'sh /datahub/src/scripts/run-unit-tests.sh'."
echo "*** Run integration tests with 'sh /datahub/src/scripts/run-integration-tests.sh'."
echo "*** Run functional tests with 'sh /datahub/src/scripts/run-functional-tests.sh'."
echo "*** Run specific tests with commands like 'python manage.py test core'."
echo "*** Run a debuggable server with 'python manage.py runserver 0.0.0.0:8000'."
echo "***"
echo "*** For your benefit, those three commands are already part of this login session's Bash history."
(set -x; docker run -ti --rm \
    -e "DATAHUB_DOCKER_TESTING=true" \
    -e "DJANGO_LIVE_TEST_SERVER_ADDRESS=0.0.0.0:8000" \
    --volumes-from logs \
    --volumes-from data \
    --net=datahub_dev \
    -v /vagrant:/datahub \
    -w /datahub/src \
    datahuborg/datahub /bin/bash)
echo "Bringing back app container..."
(set -x; docker start app)
