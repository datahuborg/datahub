#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

if `docker inspect -f {{.State.Running}} db`; then
    echo "Starting pgcli container..."
    (set -x; docker run -ti --rm \
        --net=datahub_dev \
        diyan/pgcli --host db --user postgres -w)
    echo "Closing pgcli container."
else
    echo "db container not running. Skipping pgcli."
fi
