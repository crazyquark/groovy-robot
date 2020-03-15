#!/bin/bash
PID=`cat server.pid`

`wget http://localhost:8080/halt -O /dev/null`
sleep 2

kill -9  $PID

