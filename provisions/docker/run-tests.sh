echo "Creating testing environment"
docker run -ti --rm \
    --link db:db \
    --link web:web \
    --link phantomjs:phantomjs \
    -e "datahub_docker_testing=true" \
    -v /vagrant:/datahub \
    datahuborg/datahub /bin/bash -c 
    "cd src && \
    python manage.py test functional_tests.test_login_auth "