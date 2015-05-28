#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

rm -rf $abspath/gen-py

thrift --gen py -o $abspath $abspath/thrift/datahub.thrift
thrift --gen py -o $abspath $abspath/thrift/account.thrift

# generate C++ apis
( exec $abspath"/examples/cpp/setup.sh" )

# generate Go apis
( exec $abspath"/examples/go/setup.sh" )

# generate java apis
( exec $abspath"/examples/java/setup.sh")

# generate javascript apis
# ( exec $abspath"/examples/javascript/setup.sh")



PYTHONPATH=$abspath:$abspath/gen-py:$abspath/apps
export PYTHONPATH