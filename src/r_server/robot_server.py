import platform

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

		# Attempting to limit max speed to avoid crashes
		self.maxSpeed = 95

		# Check if this is the real deal
		arch = platform.uname()[4]
		self.runningOnPi = True if arch.startswith('arm') else False

		self.setupGrovePi()

	def setupGrovePi(self):
		if not self.runningOnPi:
			return

		from grovepi_driver.grove_i2c_motor_driver import motor_driver as motorDriver

		self.motors = motorDriver()

	def speedAdjust(self, amount):
		print 'SPEED: ' + str(amount)
		self.speed += amount

		if self.speed >= self.maxSpeed:
			self.speed = self.maxSpeed
		elif self.speed <= 0:
			self.speed = 0

		self.motors.MotorSpeedSetAB(self.speed,self.speed)

	def move(self, dir):
		print('MOVE: ', dir)

		if not self.runningOnPi:
			return
		
		if dir == 1:
			self.motors.MotorDirectionSet(self.forwardDir)
		elif dir == -1:
			self.motors.MotorDirectionSet(self.backwardDir)
		elif dir == 2:
			self.motors.MotorDirectionSet(self.leftDir)
		elif dir == 3:
			self.motors.MotorDirectionSet(self.rightDir)
		
		self.motors.MotorSpeedSetAB(self.speed,self.speed)

	def stop(self):
		print('STOP')

		if not self.runningOnPi:
			return

		self.motors.MotorSpeedSetAB(0,0)
		