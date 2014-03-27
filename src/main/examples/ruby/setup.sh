#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../../../.."; pwd)

rm -rf $abspath/gen-rb
thrift --gen rb -o $abspath $basepath/src/main/datahub.thrift
