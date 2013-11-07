#!/bin/sh
abspath=$(cd "$(dirname "$0")"; pwd)
rm -rf $abspath/gen-py
thrift --gen py -o $abspath $abspath/datahub.thrift
PYTHONPATH=$PYTHONPATH:$abspath/gen-py:$abspath
export PYTHONPATH