#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../../../.."; pwd)

rm -rf $abspath/gen-js
thrift --gen rb -o $abspath $basepath/src/datahub/datahub.thrift