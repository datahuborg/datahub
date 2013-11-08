#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
rm -rf $abspath/gen-js
thrift --gen js -o $abspath $abspath/../../datahub.thrift