#!/bin/bash

# Also: enable camera and i2c

echo 'apt install'
sudo apt update
sudo apt upgrade -y
sudo apt install -y avahi-daemon

sudo apt install -y git
sudo apt install -y i2c-tools
sudo apt install -y python3
sudo apt install -y python3-pip
sudo apt install -y python3-pil
sudo apt install -y python3-numpy
sudo apt install -y python3-smbus
sudo apt install -y python3-evdev
sudo apt install -y python3-pyaudio
sudo apt install -y python3-cffi
sudo apt install -y python3-gevent
sudo apt install -y libusb-1.0.0-dev
sudo apt install -y joystick
sudo apt install -y libbluetooth-dev 
sudo apt install -y pkg-config
sudo apt install -y python3-libgpiod
sudo apt install -y swig
# maybe:
# sudo apt install -y python3-opencv
# sudo apt install -y bluez

echo 'pip3'
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo 'pixy2'
pushd lib/pixy2/scripts
export PYTHON=python3
. ./build_all.sh
unset PYTHON
pushd ../src/host/linux
sudo cp pixy.rules /etc/udev/rules.d/
popd

echo 'nvm'
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
