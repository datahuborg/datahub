#!/bin/sh
rm -rf $abspath/nohup.out

process_line=`lsof -i :9000 | tail -1`
if [ "$process_line" != "" ]; then
    process_name=`echo "$process_line" | awk '{print $1}'`
    echo "killing $process_name"
    sudo kill `echo "$process_line" | awk '{print $2}'`
fi

nohup python $abspath/server.py &