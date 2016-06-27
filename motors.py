#!/usr/bin/env python
#
# GrovePi Example for using the Grove - I2C Motor Driver(http://www.seeedstudio.com/depot/Grove-I2C-Motor-Driver-p-907.html)
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# NOTE:
# 	* Refer to the wiki to make sure that the address is correct: http://www.seeedstudio.com/wiki/Grove_-_I2C_Motor_Driver_V1.3 
#	* The I2C motor driver is very sensitive to the commands being sent to it
#	* Do not run i2cdetect or send a wrong command to it, the motor driver will stop working and also pull down the I2C clock line, which makes the GrovePi or any other device to stop working too
#	*Press reset when if you keep getting errors
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''



import time
import signal
import sys
import pygame

# VS Debug support
from ptvsd import enable_attach as enableAttach
enableAttach('kriekpi') 

class Robot:
	def __init__(self):
		pygame.init();
		self.screen = pygame.display.set_mode((640,480))

		signal.signal(signal.SIGINT, self.signalHandler)

		# Check if we're on an RPi
		self.runningOnPi = True
		try:
			import grove_i2c_motor_driver as motorDriver
		except:
			self.runningOnPi = False

		self.setupMotors()

	def signalHandler(self,_):
		print('Bye!')
		sys.exit(0)

	def setupMotors(self):
		try:
			# You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)
			if self.runningOnPi:
				m = motorDriver.motor_driver()
			else:
				m = ''

			while True:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_a:
							self.left(m)
						elif event.key == pygame.K_d:
							self.right(m)
						elif event.key == pygame.K_w:
							self.forward(m)
						elif event.key == pygame.K_s:
							self.backward(m)
					elif event.type == pygame.KEYUP:
						self.stop(m)
		except IOError as e:
			print('Unable to find the motor driver, check the addrees and press reset on the motor driver and try again')
			print('I/O error({0}): {1}'.format(e.errno, e.strerror))
	
	def left(self, m):
		print('LEFT')

		if not self.runningOnPi:
			return

		m.MotorSpeedSetAB(100,100)	#defines the speed of motor 1 and motor 2;
		m.MotorDirectionSet(0b1001)	#'0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'
	
	def right(self, m):
		print('RIGHT')

		if not self.runningOnPi:
			return

		m.MotorSpeedSetAB(100,100)	#defines the speed of motor 1 and motor 2;
		m.MotorDirectionSet(0b0110)	#'0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'

	def forward(self, m):
		print('FORWARD')

		if not self.runningOnPi:
			return

		m.MotorSpeedSetAB(100,100)	#defines the speed of motor 1 and motor 2;
		m.MotorDirectionSet(0b1010)	#'0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'

	def backward(self, m):
		print('BACKWARD')

		if not self.runningOnPi:
			return

		m.MotorSpeedSetAB(100,100)	#defines the speed of motor 1 and motor 2;
		m.MotorDirectionSet(0b0101)	#'0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'

	def stop(self, m):
		print('STOP')

		if not self.runningOnPi:
			return

		m.MotorSpeedSetAB(0,0)

if __name__ == '__main__':
	robbie = Robot()