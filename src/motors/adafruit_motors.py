'''
    Adafruit DC HAT implementation for Motors
'''
import atexit

try:
    from adafruit_blinka import agnostic
    # hack for Odroid
    agnostic.board_id = 'raspi_3'
    
    from adafruit_motorkit import MotorKit
except:
    print('Adafruit Motor HAT lib is not available')

from .motors import Motors

class AdafruitMotors(Motors):
    '''
        Motors implementation for the Adafruit DC & Stepper HAT
    '''
    default_speed = 170

    def __init__(self, addr=0x60, left_id=2, right_id=1, left_trim=0, right_trim=0):
        Motors.__init__(self, left_trim=left_trim, right_trim=right_trim)

        # Scale for [-1, 1] range
        self.left_trim = float(self.left_trim) / 100.0
        self.right_trim = float(self.right_trim) / 100.0

        # Start at ~60% speed
        self.speed = AdafruitMotors.default_speed

        # Speed values are in [-1.0, 1.0]
        self.max_speed = 1.0

        # We need to make the motors stateful
        # They don't seem to deal well with quick on/off actions
        self.power_left = 0
        self.power_right = 0

        self.speed_changed = False

        if self.running_on_arm:
            # default I2C address is 0x60
            self.motors = MotorKit()

            # dc motors
            self.right_motor = self.motors.motor1
            self.left_motor = self.motors.motor2

            # stepper
            self.stepper = self.motors.stepper2

            # Start with motors turned off.
            self.left_motor.throttle = 0.0
            self.right_motor.throttle = 0.0

            # Configure all motors to stop at program exit if desired.
            atexit.register(self.stop)
        else:
            self.motors = None

    def step(self, _):
        pass

    def control_motors(self, power_left, power_right):
        if self.running_on_arm:
            if power_left == power_right == 0:
                return self.stop()

            if self.power_left != power_left or self.speed_changed:
                # Adjust left motor if we have to
                self.power_left = float(power_left) / 100.0 + self.left_trim
                self.left_motor.throttle = self.power_left
            if self.power_right != power_right or self.speed_changed:
                # Same for right motor
                self.power_right = float(power_right) / 100.0 + self.right_trim
                self.right_motor.throttle = self.power_right
            # Reset flag
            self.speed_changed = False

    def set_speed(self, speed):
        '''
            Set speed to a given amount
        '''
        if speed == None:
            speed = AdafruitMotors.default_speed
        
        Motors.set_speed(self, speed)
        self.speed_changed = True

    def stop(self):
        if self.running_on_arm:
            # Kill power
            self.left_motor.throttle = 0.0
            self.right_motor.throttle = 0.0

            self.power_left = self.power_right = 0.0
