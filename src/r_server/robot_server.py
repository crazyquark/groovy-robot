import platform, threading, sys, traceback, time

class Directions:
	Forward, Back, Left, Right = range(4)

class Throttle:
	Up, Down = (1, -1)

class RobotServer(object):
	'''Server component for controlling a local GrovePi based robot'''
	def __init__(self):
		# Motor directions
		# '0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'
		self.forwardDir  = 0b0101
		self.backwardDir = 0b1010
		self.rightDir	 = 0b1001
		self.leftDir	 = 0b0110

		self.fwdPressed = False
		self.backPressed = False
		self.leftPressed = False
		self.rightPressed = False

		self.speed = 75 # 75% power output
		self.turnFactor = 2 # controls how sharp the turns will be

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
				try:	
					if ((not self.forwardDir and not self.backPressed and  not self.leftPressed and not self.rightPressed) or
						(self.fwdPressed and self.backPressed) or (self.leftPressed and self.rightPressed)):
						# Full stop
						self.motors.MotorSpeedSetAB(0, 0)
					elif (not self.leftPressed and not self.rightPressed and self.fwdPressed):
						# Full steam ahead!
						self.motors.MotorDirectionSet(self.forwardDir)
						self.motors.MotorSpeedSetAB(self.speed, self.speed)
					elif (not self.leftPressed and not self.rightPressed and self.backPressed):
						# All engines reverse!
						self.motors.MotorDirectionSet(self.backwardDir)
						self.motors.MotorSpeedSetAB(self.speed, self.speed)
					elif (not self.backPressed and not self.fwdPressed and self.rightPressed):
						# In place right turn
						self.motors.MotorDirectionSet(self.rightDir)
						self.motors.MotorSpeedSetAB(self.speed, self.speed)
					elif (not self.backPressed and not self.fwdPressed and self.leftPressed):
						# In place left turn
						self.motors.MotorDirectionSet(self.leftDir)
						self.motors.MotorSpeedSetAB(self.speed, self.speed)
					elif ((self.fwdPressed or self.backPressed) and self.rightPressed):
						# Attempt to turn right
						self.motors.MotorDirectionSet(self.forwardDir if self.fwdPressed else self.backwardDir)
						self.motors.MotorSpeedSetAB(self.speed, self.speed / self.turnFactor)
					elif ((self.fwdPressed or self.backPressed) and self.leftPressed):
						# Attempt to turn left
						self.motors.MotorDirectionSet(self.forwardDir if self.fwdPressed else self.backwardDir)
						self.motors.MotorSpeedSetAB(self.speed / self.turnFactor, self.speed)
					else:
						# I donno
						self.motors.MotorSpeedSetAB(0, 0)
				except:
					print 'Critical failure, shutting down'
					print 'Possible cause: '
					traceback.print_exc()
					self.runnig = False
					raise Exception('Motors failure')
					
	def setupGrovePi(self):
		if not self.runningOnPi:
			return

		from grovepi_driver.grove_i2c_motor_driver import motor_driver as motorDriver

		self.motors = motorDriver()

		import grove_oled as oledDisplay
		self.oledDisplay = oledDisplay

		oledDisplay.oled_init()
		oledDisplay.oled_clearDisplay()
		oledDisplay.oled_setNormalDisplay()
		time.sleep(.1)

		oledDisplay.oled_setTextXY(0,0)
		oledDisplay.oled_putString("Robot Ready!")

	def speedAdjust(self, dir):
		amount = dir * self.speedIncrement
		self.speed += amount

		if self.speed >= self.maxSpeed:
			self.speed = self.maxSpeed
		elif self.speed <= 0:
			self.speed = 0

		print('SPEED: ', self.speed)

	def processPress(self, dir, isOn):
		if dir == Directions.Forward:
			self.fwdPressed = isOn
		elif dir == Directions.Back:
			self.backPressed = isOn
		elif dir == Directions.Left:
			self.leftPressed = isOn
		elif dir == Directions.Right:
			self.rightPressed = isOn	

	def move(self, dir):
		print('MOVE: ', dir)

		if not self.runningOnPi:
			return
		
		self.processPress(dir, True)

	def stop(self, dir):
		print('STOP: ', dir)

		if not self.runningOnPi:
			return

		self.processPress(dir, False)

	def halt(self):
		self.running = False
		