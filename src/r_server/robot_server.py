import platform, sys, traceback, time
from threading import Thread

from motors.adafruit_motors import AdafruitMotors

class Directions:
    Forward, Back, Left, Right = range(4)

class Throttle:
    Up, Down = (1, -1)

class RobotServer(Thread):
    '''
        Server component for controlling a local GrovePi based robot
        Uses an autostart thread to run its update loop
    '''
    def __init__(self):
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

        if self.runningOnPi:
            self.motors = AdafruitMotors()
        
        Thread.__init__(self)
        self.running = True
        self.start()
        
    def run(self):
        while(self.running):
            if (self.runningOnPi):
                try:	
                    if ((not self.fwdPressed and not self.backPressed and not self.leftPressed and not self.rightPressed) or
                        (self.fwdPressed and self.backPressed) or (self.leftPressed and self.rightPressed)):
                        # Full stop
                        self.motors.control_motors(0, 0)
                    elif (not self.leftPressed and not self.rightPressed and self.fwdPressed):
                        # Full steam ahead!
                        self.motors.control_motors(100, 100)
                    elif (not self.leftPressed and not self.rightPressed and self.backPressed):
                        # All engines reverse!
                        self.motors.control_motors(-100, -100)
                    elif (not self.backPressed and not self.fwdPressed and self.rightPressed):
                        # In place right turn
                        self.motors.control_motors(-100, 100)
                    elif (not self.backPressed and not self.fwdPressed and self.leftPressed):
                        # In place left turn
                        self.motors.control_motors(100, -100)
                    elif ((self.fwdPressed or self.backPressed) and self.rightPressed):
                        # Attempt to turn right
                        self.motors.control_motors(100 / self.turnFactor, 100)
                    elif ((self.fwdPressed or self.backPressed) and self.leftPressed):
                        # Attempt to turn left
                        self.motors.control_motors(100, 100 / self.turnFactor)
                    else:
                        # I donno
                        self.motors.MotorSpeedSetAB(0, 0)
                except:
                    print 'Critical failure, shutting down'
                    print 'Possible cause: '
                    traceback.print_exc()
                    self.runnig = False
                    raise Exception('Motors failure')

    def speedAdjust(self, direction):
        if self.runningOnPi:
            amount = direction * self.speedIncrement
            self.motors.change_speed(amount)

    def processPress(self, direction, isOn):
        if direction == Directions.Forward:
            self.fwdPressed = isOn
        elif direction == Directions.Back:
            self.backPressed = isOn
        elif direction == Directions.Left:
            self.leftPressed = isOn
        elif direction == Directions.Right:
            self.rightPressed = isOn	

    def move(self, direction):
        print('MOVE: ', dir)

        if not self.runningOnPi:
            return
        
        self.processPress(direction, True)

    def stop(self, direction):
        print('STOP: ', direction)

        if not self.runningOnPi:
            return

        self.processPress(direction, False)

    def halt(self):
        self.running = False
        