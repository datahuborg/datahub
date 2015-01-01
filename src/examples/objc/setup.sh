#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
basepath=$(cd "$abspath/../.."; pwd)

rm -rf $abspath/gen-cocoa

thrift --gen cocoa -o $abspath $basepath/datahub.thrift