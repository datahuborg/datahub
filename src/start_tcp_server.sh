#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

source $abspath/stop_tcp_server.sh

echo "Starting DataHub TCP server..."
nohup python $abspath/server.py > /dev/null 2>&1 &
echo "Done."