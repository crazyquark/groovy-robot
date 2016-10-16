#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR/src
PID=`cat server.pid`
sudo pkill -TERM -P $PID
popd

