#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

(set -x; docker run --rm -t \
    --volumes-from app \
    datahuborg/datahub \
    /bin/bash -c \
    "make html && python src/manage.py collectstatic --noinput")
