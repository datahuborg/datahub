echo "Starting phantomjs container..."
if ! `docker inspect -f {{.State.Running}} phantomjs`; then
    (set -x; docker start phantomjs)
    echo "phantomjs started."
else
    echo "phantomjs already running. Skipping."
fi
echo "Creating testing container..."
(set -x; docker run -ti --rm \
    --link db:db \
    --link phantomjs:phantomjs \
    -e "DATAHUB_DOCKER_TESTING=true" \
    -v /vagrant:/datahub \
    datahuborg/datahub /bin/bash)
