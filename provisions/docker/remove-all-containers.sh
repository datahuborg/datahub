#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

CONTAINERS=`docker ps -a --format '{{.Names}}'`

# Build the project's Docker images if you don't want to pull the prebuilt ones from Docker Hub
echo "Are you sure you want to delete the Docker containers: "$CONTAINERS"? [y,N]"
read input
if [[ $input == "Y" || $input == "y" ]]; then
        set -x; docker rm -f $CONTAINERS
fi
