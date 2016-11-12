#!/bin/bash

# Compile mjpeg-streamer
pushd lib/mjpg-streamer/mjpg-streamer-experimental
make
popd

# Install deps
sudo pip install -r requirements.txt
