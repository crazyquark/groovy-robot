#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR/src
PID=`cat server.pid`
kill -9 $PID
popd

