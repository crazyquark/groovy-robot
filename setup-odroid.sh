#!/bin/bash
# Adapted for Armbian Buster
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
sudo apt install -y libusb-dev
sudo apt install -y joystick
sudo apt install -y libbluetooth-dev 
sudo apt install -y pkg-config
sudo apt install -y checkinstall
sudo apt install -y linux-headers-current-meson64
sudo apt install -y python3-libgpiod
# maybe:
# sudo apt install -y python3-opencv
# sudo apt install -y bluez

sudo adduser $USER i2c

git clone https://github.com/jfath/RPi.GPIO-Odroid.git
pushd RPi.GPIO-Odroid
sudo python3 setup.py build install
popd
rm -rf RPi.GPIO-Odroid

echo 'sixad'
git clone https://github.com/RetroPie/sixad.git
pushd sixad
make
mkdir -p /var/lib/sixad/profiles
sudo checkinstall
popd
rm -rf sixad

echo 'pip3'
pip3 install --upgrade pip
pip3 install -r requirements.txt

echo 'gpio'
sudo cp ./config/97-gpio.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger

