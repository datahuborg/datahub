#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../../../.."; pwd)

rm -rf $abspath/gen-js
thrift --gen php -o $abspath $basepath/src/main/datahub.thrift
