#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pushd $DIR/src
python3 server.py &> ../server.log & 
echo $! > ../server.pid
popd
