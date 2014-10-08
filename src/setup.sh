#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

rm -rf $abspath/gen-py
thrift --gen py -o $abspath $abspath/datahub.thrift
PYTHONPATH=$abspath:$abspath/gen-py:$abspath/apps
export PYTHONPATH