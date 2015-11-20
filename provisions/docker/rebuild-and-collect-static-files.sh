#!/bin/bash
docker run --rm -t --volumes-from app datahuborg/datahub /bin/bash -c "make html && python src/manage.py collectstatic --noinput"
