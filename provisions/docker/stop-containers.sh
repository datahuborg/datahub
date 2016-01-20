#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

echo "Stopping containers..."
docker stop web
docker stop app
docker stop db
echo "Done."