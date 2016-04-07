#!/bin/bash

if (( EUID != 0 )); then
   echo "Script must be run as root."
   exit 126
fi

COMMAND="help"

if [[ ! -z "$1" ]]; then
    COMMAND="$1"
fi

# Build the project's Docker images if you don't want to pull the prebuilt ones from Docker Hub
echo "Analyzing project with local codeclimate..."
pushd /vagrant/
(set -x;
docker run \
  --interactive --tty --rm \
  --env CODECLIMATE_CODE="$PWD" \
  --volume "$PWD":/code \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  --volume /tmp/cc:/tmp/cc \
  codeclimate/codeclimate $COMMAND)
popd
