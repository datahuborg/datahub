#!/bin/bash

# Build the project's Docker images if you don't want to pull the prebuilt ones from Docker Hub
echo "Building Docker images..."
echo "Building datahuborg/postgres (1/4)"
docker build -t datahuborg/postgres provisions/postgres/
echo "Building datahuborg/nginx (2/4)"
docker build -t datahuborg/nginx provisions/nginx/
echo "Building datahuborg/datahub (3/4)"
docker build -t datahuborg/datahub .
echo "Pulling latest phantomjs (4/4)"
docker pull wernight/phantomjs:latest
echo "Done."