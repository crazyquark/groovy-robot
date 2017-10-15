'''
    Motor drivers available: Adafruit DC Motors Hat and GrovePi motor module
'''

class Motors(object):
    '''
        Generic motors implementation
    '''
    def __init__(self):
        self.speed = 0

        # Attempting to limit max speed to avoid crashes
        self.max_speed = 95

        from platform import uname
        self.running_on_pi = uname()[4].startswith('arm')

    def change_speed(self, amount):
        '''
            Increase/decrease speed
        '''
        print 'SPEED: ' + str(amount)
        self.speed += amount

        if self.speed >= self.max_speed:
            self.speed = self.max_speed
        elif self.speed <= 0:
            self.speed = 0

    def control_motors(self, left_power, right_power):
        '''
            Control the 2 motors independetly by applying a power factor
        '''
        if not self.running_on_pi:
            return

    def stop(self):
        '''
            Emergency stop
        '''
        self.speed = 0

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

    def control_motors(self, left_power, right_power):
        Motors.left(self)

        self.motors.MotorSpeedSetAB(self.speed * abs(left_power), self.speed * abs(right_power))
        if left_power >= left_power and right_power >= 0:
            self.motors.MotorDirectionSet(self.forward_dir)
        elif left_power < 0 and right_power < 0:
            self.motors.MotorDirectionSet(self.backward_dir)
        elif left_power < 0 and right_power >= 0:
            self.motors.MotorDirectionSet(self.right_dir)
        elif left_power >= 0 and right_power < 0:
            self.motors.MotorDirectionSet(self.left_dir)
