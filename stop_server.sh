#!/bin/bash
PID=`cat server.pid`

`wget http://localhost:8080/halt`
sleep 2

kill -9  $PID

