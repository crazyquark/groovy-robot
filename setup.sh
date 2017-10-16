#!/bin/bash

# On Dietpi this is needed:
apt install python-dev
easy_install pip
apt install python-pygame

pushd lib/adafruit_motor_hat
python setup.py install
popd

# Install deps
sudo pip install -r requirements.txt
