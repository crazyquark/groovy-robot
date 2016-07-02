import os

class RobotServer(object):
	"""Server component for controlling a local GrovePi based robot"""
	def __init__(self):
		# Motor directions
		# '0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'
		self.forwardDir  = 0b0101
		self.backwardDir = 0b1010
		self.rightDir	 = 0b1001
		self.leftDir	 = 0b0110

		self.speed = 75 # 75% power output

		# Check if this is the real deal
		arch = os.uname()[4]
		self.onPi = True if arch.startswith('arm') else False

		setupGrovePi()

	def setupGrovePi(self):
		if not self.onPi:
			return

		from grovepi_driver.grove_i2c_motor_driver import motor_driver as motorDriver

		self.motors = motorDriver()

	def speedAdjust(self, amount):
		print 'SPEED: ' + str(amount)
		self.speed += amount

		if self.speed >= 100:
			self.speed = 100
		elif self.speed <= 0:
			self.speed = 0

	def forward(self, m):
		print('FORWARD')

		if not runningOnPi:
			return

		m.MotorSpeedSetAB(self.speed,self.speed)	
		m.MotorDirectionSet(self.forwardDir)	

	def stop(self, m):
		print('STOP')

		if not runningOnPi:
			return

		m.MotorSpeedSetAB(0,0)
		