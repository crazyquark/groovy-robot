'''
    GrovePi Motors implementation
'''
try:
    from grovepi_driver.grove_i2c_motor_driver import motor_driver
except:
    print('GrovePi motors lib is not available')

from motors import Motors

class GrovePiMotors(Motors):
    '''
        The GrovePi implementation
    '''
    def __init__(self, running_on_arm):
        Motors.__init__(self, running_on_arm)

        # Directions
        # '0b1010' defines the output polarity,
        # '10' means the M+ is 'positive' while the M- is 'negative'
        self.forward_dir = 0b0101
        self.backward_dir = 0b1010
        self.left_dir = 0b1001
        self.right_dir = 0b0110

        if self.running_on_arm:
            # You can initialize with a different address too:
            # grove_i2c_motor_driver.motor_driver(address=0x0a)
            self.motors = motor_driver()
        else:
            self.motors = None

    def control_motors(self, left_power, right_power):
        Motors.control_motors(self, left_power, right_power)

        self.motors.MotorSpeedSetAB(self.speed * abs(left_power), self.speed * abs(right_power))
        if left_power >= left_power and right_power >= 0:
            self.motors.MotorDirectionSet(self.forward_dir)
        elif left_power < 0 and right_power < 0:
            self.motors.MotorDirectionSet(self.backward_dir)
        elif left_power < 0 and right_power >= 0:
            self.motors.MotorDirectionSet(self.right_dir)
        elif left_power >= 0 and right_power < 0:
            self.motors.MotorDirectionSet(self.left_dir)
