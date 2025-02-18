'''
    Adafruit DC HAT implementation for Motors
'''
import atexit
import math

from adafruit_motor import stepper
try:
    from adafruit_motorkit import MotorKit
except:
    print('Not running on a supported board for Adafruit''s MotorKit')

from .motors import Motors


class StepperDirections:
    Forward = stepper.FORWARD
    Backward = stepper.BACKWARD


class AdafruitMotors(Motors):
    '''
        Motors implementation for the Adafruit DC & Stepper HAT
    '''
    default_speed = 1.0

    def __init__(self, running_on_arm, addr=0x60, left_id=2, right_id=1, left_trim=0, right_trim=0):
        Motors.__init__(self, left_trim=left_trim,
                        right_trim=right_trim, running_on_arm=running_on_arm)
        # Start at 100% speed
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
            self.motors = MotorKit(steppers_microsteps=32)

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

    def step(self, dir):
        self.stepper.onestep(direction=dir, style=stepper.DOUBLE)

    def control_motors(self, power_left, power_right):
        if power_left == power_right == 0:
            return self.stop()

        if self.power_left != power_left or self.speed_changed:
            # Adjust left motor if we have to
            self.power_left = math.copysign((float(abs(power_left)) + self.left_trim) / 100.0, power_left)
            assert self.power_left >= -1.0 and self.power_left <= 1.0
            if self.running_on_arm:
                self.left_motor.throttle = self.power_left * self.speed
        if self.power_right != power_right or self.speed_changed:
            # Same for right motor
            self.power_right = math.copysign((float(abs(power_right)) + self.right_trim) / 100.0, power_right)
            assert self.power_right >= -1.0 and self.power_right <= 1.0
            if self.running_on_arm:
                self.right_motor.throttle = self.power_right * self.speed
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
            self.left_motor.throttle = None
            self.right_motor.throttle = None

            self.power_left = self.power_right = 0.0
