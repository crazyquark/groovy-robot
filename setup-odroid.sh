echo 'git & tools'
apt install git
apt install i2c-tools
apt install python3-pip
apt install python3-pil

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

echo 'modules'
echo aml_i2c >> /etc/modules
echo spicc >> /etc/modules
echo spidev >> /etc/modules
