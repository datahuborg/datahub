#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

rm -rf $abspath/gen-py

thrift --gen py -o $abspath $abspath/thrift/datahub.thrift
thrift --gen py -o $abspath $abspath/thrift/account.thrift


PYTHONPATH=$abspath:$abspath/gen-py:$abspath/apps
export PYTHONPATH

echo "---Finished setting up.---"