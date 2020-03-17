echo 'apt'
apt install -y git
apt install -y i2c-tools
apt install -y python3-pip
apt install -y python3-pil
apt install -y python3-numpy
apt install -y python3-smbus
apt install -y python3-evdev
apt install -y python3-pyaudio
apt install -y python3-cffi
apt install -y python3-opencv
apt install -y libusb-dev
apt install -y joystick
apt install -y libbluetooth-dev
apt install -y bluez
apt install -y pkg-config
apt install -y checkinstall
apt install -y swig

echo 'wiringPi'
git clone https://github.com/hardkernel/wiringPi
pushd wiringPi
./build
popd

git clone --recursive https://github.com/hardkernel/WiringPi2-Python
pushd WiringPi2-Python
python3 setup.py install
python setup.py install
popd

git clone https://github.com/jfath/RPi.GPIO-Odroid.git
pushd RPi.GPIO-Odroid
python3 setup.py build install
python setup.py build install
popd

pushd lib/adafruit_motor_hat
python3 setup.py install
popd

pushd lib/pixy2/scripts
export PYTHON=python3
. ./build_all.sh
unset PYTHON
popd

echo 'sixad'
git clone https://github.com/RetroPie/sixad.git
pushd sixad
make
mkdir -p /var/lib/sixad/profiles
checkinstall
dpkg -i sixad_*.deb
popd

echo 'modules'
echo aml_i2c >> /etc/modules
echo spicc >> /etc/modules
echo spidev >> /etc/modules

echo 'pip3'
pip3 install -r requirements.txt

