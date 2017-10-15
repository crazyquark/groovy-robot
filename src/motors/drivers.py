'''
    Motor drivers available: Adafruit DC Motors Hat and GrovePi motor module
'''

class Motors:
    '''
        Generic motors implementation
    '''
    def __init__(self):
        self.speed = 0

        # Attempting to limit max speed to avoid crashes
        self.max_speed = 95

        self.turnFactor = 2 # controls how sharp the turns will be

        from platform import uname
        self.running_on_pi = uname()[4].startswith('arm')

    def change_speed(self, amount):
        '''
            Increase/decrease speed
        '''
        print('SPEED: ' + str(amount))
        self.speed += amount

        if self.speed >= self.max_speed:
            self.speed = self.max_speed
        elif self.speed <= 0:
            self.speed = 0

    def stop(self, m):
        print('STOP')

        if not self.running_on_pi:
            return

        m.MotorSpeedSetAB(0,0)

class GrovePiMotors(Motors):
    '''
        The GrovePi implementation
    '''
    def __init__(self):
        Motors.__init__(self)

        # Directions
        # '0b1010' defines the output polarity,
        # '10' means the M+ is 'positive' while the M- is 'negative'
        self.forward_dir = 0b0101
        self.backward_dir = 0b1010
        self.left_dir = 0b1001
        self.right_dir = 0b0110

        if self.running_on_pi:
            from grovepi_driver.grove_i2c_motor_driver import motor_driver
            # You can initialize with a different address too:
            # grove_i2c_motor_driver.motor_driver(address=0x0a)
            self.motors = motor_driver() if self.running_on_pi else ''
        else:
            self.motors = None

    def left(self):
        Motors.left(self)

        self.motors.MotorSpeedSetAB(self.speed, self.speed)
        self.motors.MotorDirectionSet(self.left_dir)
    