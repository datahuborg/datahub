echo "Creating testing environment"
docker start phantomjs;
docker run -ti --rm \
    --link db:db \
    --link web:web \
    --link phantomjs:phantomjs \
    -e "USER=vagrant" \
    -e "datahub_docker_testing=true" \
    -v /vagrant:/datahub \
    datahuborg/datahub /bin/bash