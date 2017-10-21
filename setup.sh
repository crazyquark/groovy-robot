#!/bin/bash

# Also: enable camera and i2c

# Might not be needed on all distros
apt install -y build-essential
apt install -y python3-dev
apt install -y python3-pip
apt install -y python3-pygame
apt install -y python3-opencv
apt install -y python3-smbus

pushd lib/adafruit_motor_hat
python3 setup.py install
popd

# Install deps
pip3 install -r requirements.txt
