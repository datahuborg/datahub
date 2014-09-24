#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

basepath=$(cd "$abspath/../../../.."; pwd)

rm -rf $abspath/gen-nodejs
thrift --gen js:node -o $abspath $basepath/src/main/datahub.thrift

NODE_PATH=/usr/local/lib/node_modules/:$abspath/gen-nodejs
export NODE_PATH