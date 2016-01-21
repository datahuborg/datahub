#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

FILE="/tmp/$1-backup.gz"
echo "Backing up database $1 from db container into $FILE on host machine..."
if [ ! -f $FILE ]; then
    (set -x;
    docker run --rm -t --link db:db -v /tmp:/tmp datahuborg/postgres \
        /bin/bash -c \
        "pg_dump --clean --create --if-exists --host db --username postgres -d $1 | gzip > $FILE")
else
    echo "$FILE already exists. Cancelling backup."
fi
echo "Done."
