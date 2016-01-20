#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

FILE="/tmp/backup.gz"
echo "Wiping existing Postgres data and restoring from $FILE on host machine to db container..."
if [ -f $FILE ]; then
    (set -x;
    docker run --rm -t --link db:db -v /tmp:/tmp datahuborg/postgres \
        /bin/bash -c \
        "gunzip -c $FILE | psql --host db --username postgres postgres")
else
    echo "/tmp/backup.gz missing. Cancelling restore."
fi
echo "Done."
