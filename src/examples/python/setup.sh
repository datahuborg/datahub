#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
basepath=$(cd "$abspath/../.."; pwd)

rm -rf $abspath/gen-py

thrift --gen py -o $abspath $basepath/thrift/datahub.thrift
thrift --gen py -o $abspath $basepath/thrift/account.thrift

PYTHONPATH=$abspath:$abspath/gen-py:$basepath
export PYTHONPATH
