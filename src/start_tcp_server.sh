#!/bin/sh
source stop_tcp_server.sh

nohup python $abspath/server.py &