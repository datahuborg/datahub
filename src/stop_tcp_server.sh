#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

process_line=`lsof -i :9000 | tail -1`
if [ "$process_line" != "" ]; then
    process_name=`echo "$process_line" | awk '{print $1}'`
    echo "Stopping DataHub TCP server..."
    kill `echo "$process_line" | awk '{print $2}'`
    echo "Done."
else
	echo "DataHub TCP server is not running."
fi