#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

# Default use case is to run DataHub in a Vagrant VM. Nonstandard setups should run this script from the DataHub working directory.
cd /vagrant &> /dev/null

# Build the project's Docker images if you don't want to pull the prebuilt ones from Docker Hub
echo "Building Docker images..."
echo "Building datahuborg/postgres (1/4)"
docker build -t datahuborg/postgres provisions/postgres/
echo "Building datahuborg/nginx (2/4)"
docker build -t datahuborg/nginx provisions/nginx/
echo "Building datahuborg/datahub (3/4)"
# Build the base image manually if you can't pull from Docker Hub.
# docker build -t datahuborg/datahub-base -f Dockerfile-base .
docker build -t datahuborg/datahub .
echo "Pulling latest phantomjs (4/4)"
docker pull wernight/phantomjs:latest
echo "Done."