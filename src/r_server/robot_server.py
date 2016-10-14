import platform, threading

class RobotServer(object):
	"""Server component for controlling a local GrovePi based robot"""
	def __init__(self):
		# Motor directions
		# '0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'
		self.forwardDir  = 0b0101
		self.backwardDir = 0b1010
		self.rightDir	 = 0b1001
		self.leftDir	 = 0b0110

		self.currentDir  = 0b0000

		self.speed = 75 # 75% power output

		# Attempting to limit max speed to avoid crashes
		self.maxSpeed = 95
		
		# How much to increase speed at one time
		self.speedIncrement = 5

		# Check if this is the real deal
		arch = platform.uname()[4]
		self.runningOnPi = True if arch.startswith('arm') else False

		print('We are running on: ', arch)

		self.setupGrovePi()
		
		self.running = True
		updateThread = threading.Thread(target = self.update)
		updateThread.start()
		
	def update(self):
		while(self.running):
			if (self.runningOnPi):
				self.motors.MotorSpeedSetAB(self.speed,self.speed)
				self.motors.MotorDirectionSet(self.forwardDir)	

	def setupGrovePi(self):
		if not self.runningOnPi:
			return

		from grovepi_driver.grove_i2c_motor_driver import motor_driver as motorDriver

		self.motors = motorDriver()

	def speedAdjust(self, dir):
		amount = dir * self.speedIncrement
		self.speed += amount

		if self.speed >= self.maxSpeed:
			self.speed = self.maxSpeed
		elif self.speed <= 0:
			self.speed = 0

		print('SPEED: ', self.speed)

	def move(self, dir):
		print('MOVE: ', dir)

		if not self.runningOnPi:
			return
		
		if dir == 1:
			self.currentDir &= self.forwardDir
		elif dir == -1:
			self.currentDir &= self.backwardDir
		elif dir == 2:
			self.currentDir &= self.leftDir
		elif dir == 3:
			self.currentDir &= self.rightDir

	def stop(self, dir):
		print('STOP')

		if not self.runningOnPi:
			return

		self.motors.MotorSpeedSetAB(0,0)
		