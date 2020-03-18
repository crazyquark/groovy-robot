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
# sudo apt install -y python3-opencv
sudo apt install -y libusb-dev
sudo apt install -y joystick
# sudo apt install -y libbluetooth-dev
# sudo apt install -y bluez
sudo apt install -y pkg-config
sudo apt install -y checkinstall

sudo adduser $USER i2c

wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/libgpiod.sh
chmod +x libgpiod.sh
./libgpiod.sh

git clone https://github.com/jfath/RPi.GPIO-Odroid.git
pushd RPi.GPIO-Odroid
python3 setup.py build install
python setup.py build install
popd

echo 'sixad'
git clone https://github.com/RetroPie/sixad.git
pushd sixad
make
mkdir -p /var/lib/sixad/profiles
checkinstall
dpkg -i sixad_*.deb
popd

echo 'pip3'
pip3 install --upgrade pip
pip3 install -r requirements.txt

