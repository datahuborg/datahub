#!/bin/sh
basepath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

rm -rf $basepath/gen-py
thrift --gen py -o $basepath $basepath/datahub.thrift
PYTHONPATH=$basepath:$basepath/gen-py
export PYTHONPATH