#!/bin/bash

# Also: enable camera and i2c

# Might not be needed on all distros
apt install python-dev
easy_install pip
apt install python-pygame
apt install python-opencv

pushd lib/adafruit_motor_hat
python setup.py install
popd

# Install deps
sudo pip install -r requirements.txt
