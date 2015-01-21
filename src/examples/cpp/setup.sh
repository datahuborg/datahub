#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
basepath=$(cd "$abspath/../.."; pwd)

rm -rf $abspath/bin
rm -rf $abspath/gen-cpp

thrift --gen cpp -o $abspath $basepath/thrift/datahub.thrift
thrift --gen cpp -o $abspath $basepath/thrift/account.thrift
