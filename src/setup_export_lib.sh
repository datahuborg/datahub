#!/bin/sh
abspath=$(cd "$(dirname "$BASH_SOURCE")"; pwd)

thrift --gen js -out $abspath/browser/static/lib/datahub $abspath/datahub.thrift