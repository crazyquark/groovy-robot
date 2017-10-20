#!/bin/bash

# Also: enable camera and i2c

# Might not be needed on all distros
apt install python3-dev
apt install python3-pip
apt install python3-pygame
apt install python3-opencv
apt install python3-smbus

pushd lib/adafruit_motor_hat
python3 setup.py install
popd

# Install deps
sudo pip3 install -r requirements.txt
