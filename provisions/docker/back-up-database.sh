echo "Backing up database from db container into /tmp/backup.gz on host machine..."
if [ ! -f /tmp/backup.gz ]; then
    docker run --rm -t --link db:db -v /tmp:/tmp datahuborg/postgres \
        /bin/bash -c "pg_dumpall --clean --if-exists --host db --username postgres | gzip > /tmp/backup.gz"
else
    echo "/tmp/backup.gz already exists. Cancelling backup."
fi
echo "Done."
