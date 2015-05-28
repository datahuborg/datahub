#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

rm -rf $abspath/gen-py

thrift --gen py -o $abspath $abspath/thrift/datahub.thrift
thrift --gen py -o $abspath $abspath/thrift/account.thrift

# generate C++ Code
( exec $abspath"/examples/cpp/setup.sh" )

# generate Go Code
# ( exec $abspath"/examples/go/setup.sh" )


PYTHONPATH=$abspath:$abspath/gen-py:$abspath/apps
export PYTHONPATH