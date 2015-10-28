#!/bin/bash

DIR=$(cd "$(dirname "$0")" && pwd)

sh $DIR/build-images.sh
sh $DIR/create-containers.sh
sh $DIR/start-containers.sh
