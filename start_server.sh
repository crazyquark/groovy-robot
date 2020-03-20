#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export FLASK_ENV=development
export FLASK_APP=r_server.web_server
pushd $DIR/src
python3 -m flask run --host=0.0.0.0 --port=8080
