#!/bin/bash

# Also: enable camera and i2c

# Might not be needed on all distros
sudo apt install -y build-essential
sudo apt install -y python3-dev
sudo apt install -y python3-pip
#apt install -y python3-pygame
#apt install -y python3-opencv
sudo apt install -y python3-smbus

pushd lib/adafruit_motor_hat
python3 setup.py install
popd

# Install deps
pip3 install -r requirements.txt
