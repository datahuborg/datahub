#!/bin/bash

echo "Stopping containers..."
docker stop web
docker stop app
docker stop db
echo "Done."