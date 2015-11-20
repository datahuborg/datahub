#!/bin/bash

# Build the project's Docker images if you don't want to pull the prebuilt ones from Docker Hub
echo "Building Docker images..."
echo "Building datahuborg/postgres (1/3)"
docker build -t datahuborg/postgres provisions/postgres/
echo "Building datahuborg/nginx (2/3)"
docker build -t datahuborg/nginx provisions/nginx/
echo "Building datahuborg/datahub (3/3)"
docker build -t datahuborg/datahub .
echo "Done."