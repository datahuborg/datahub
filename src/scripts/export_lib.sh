#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)
basepath=$(cd "$abspath/.."; pwd)

thrift --gen js -out $basepath/browser/static/lib/datahub $basepath/thrift/datahub.thrift