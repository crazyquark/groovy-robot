#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

pushd $DIR/src
python3 -m r_server.web_server
echo $! > server.pid
