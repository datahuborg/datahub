#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../.."; pwd)

rm -rf $abspath/gen-py
thrift --gen py -o $abspath $basepath/src/main/datahub.thrift
PYTHONPATH=$abspath:$abspath/gen-py:$basepath/src/main
export PYTHONPATH