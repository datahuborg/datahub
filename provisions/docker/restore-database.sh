echo "Wiping existing Postgres data and restoring from /tmp/backup.gz on host machine to db container..."
if [ -f /tmp/backup.gz ]; then
    docker run --rm -t --link db:db -v /tmp:/tmp datahuborg/postgres \
        /bin/bash -c \
        "gunzip -c /tmp/backup.gz | psql --host db --username postgres postgres"
else
    echo "/tmp/backup.gz missing. Cancelling restore."
fi
echo "Done."
