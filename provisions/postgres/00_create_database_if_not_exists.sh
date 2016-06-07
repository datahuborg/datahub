#!/bin/bash

TEST=`gosu postgres psql <<- EOSQL
    SELECT 1 FROM pg_database WHERE datname='$DB_NAME';
EOSQL`

echo "******CREATING DOCKER DATABASE******"
if [[ $TEST == "1" ]]; then
    echo "******DOCKER DATABASE ALREADY EXISTS******"
    # database exists
    # $? is 0
    exit 0
else
gosu postgres psql <<- EOSQL
    CREATE DATABASE $DB_NAME WITH OWNER $DB_USER TEMPLATE template0 ENCODING 'UTF8';

    # remove the public schema from the template that
    # dh user databases are created from
    \c template1;
    DROP SCHEMA PUBLIC;
    SET SEARCH_PATH TO \"$user\";
EOSQL
    echo "******DOCKER DATABASE CREATED******"
fi

echo ""
    # CREATE ROLE $DB_USER WITH LOGIN ENCRYPTED PASSWORD '${DB_PASS}' CREATEDB;
    # GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
