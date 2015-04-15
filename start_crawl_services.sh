#!/bin/bash

cd "$(dirname "$0")"
export PYTHONPATH=`pwd`
echo "Starting scrapyd..."
rm /memex-pinterest/twistd.pid | true
scrapyd --pidfile=./twistd.pid &
sleep 15
scrapyd-deploy -p profiler-project