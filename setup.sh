#!/bin/bash

# Also: enable camera and i2c

# Might not be needed on all distros
sudo apt install -y build-essential
sudo apt install -y python3-dev
sudo apt install -y python3-pip
#apt install -y python3-pygame
#apt install -y python3-opencv
sudo apt install -y python3-smbus
sudo apt install -y python3-evdev
sudo apt install -y python3-pil
sudo apt install -y python3-pyaudio

# Also see https://github.com/Arkq/bluez-alsa
# for configuration
sudo apt install bluealsa

pushd lib/adafruit_motor_hat
python3 setup.py install
popd

pushd lib/Adafruit_Python_SSD1306
python3 setup.py install
popd

# Install deps
pip3 install -r requirements.txt
