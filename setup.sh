#!/bin/bash

# Compile mjpeg-streamer
sudo apt-get install cmake libjpeg8-dev

pushd lib/mjpg-streamer/mjpg-streamer-experimental
make
popd

# Install deps
sudo pip install -r requirements.txt
