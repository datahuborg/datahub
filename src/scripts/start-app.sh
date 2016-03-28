#!/bin/bash
set -e

echo "Generating Thrift files..."
pushd /datahub/
source src/setup.sh
popd
echo "Starting Gunicorn..."
exec gunicorn browser.wsgi \
    --config=provisions/gunicorn/config_dev.py
echo "Exiting container..."
