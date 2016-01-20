#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

FILE="/tmp/backup.gz"
echo "Backing up all databases from db container into $FILE on host machine..."
if [ ! -f $FILE ]; then
    (set -x;
    docker run --rm -t --link db:db -v /tmp:/tmp datahuborg/postgres \
        /bin/bash -c \
        "pg_dumpall --clean --if-exists --host db --username postgres | gzip > $FILE")
else
    echo "$FILE already exists. Cancelling backup."
fi
echo "Done."
