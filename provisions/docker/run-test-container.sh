echo "Starting phantomjs container..."
if ! `docker inspect -f {{.State.Running}} phantomjs`; then
    (set -x; docker start phantomjs)
    echo "phantomjs started."
else
    echo "phantomjs already running. Skipping."
fi
echo "Removing dev app container..."
(set -x; docker rm -f app)
echo "Spinning up test app container..."
(set -x; docker run -ti --rm \
    -e "DATAHUB_DOCKER_TESTING=true" \
    -e "DJANGO_LIVE_TEST_SERVER_ADDRESS=0.0.0.0:8000" \
    --volumes-from logs \
    --volumes-from data \
    --net=datahub_dev \
    -v /vagrant:/datahub \
    -w /datahub/src \
    datahuborg/datahub /bin/bash)
echo "Bringing back dev app container..."
(set -x; docker create --name app \
    --env 'USER=vagrant' \
    --volumes-from logs \
    --volumes-from data \
    --net=datahub_dev \
    -v /vagrant:/datahub \
    datahuborg/datahub gunicorn --config=provisions/gunicorn/config_dev.py browser.wsgi)
(set -x; docker start app)
