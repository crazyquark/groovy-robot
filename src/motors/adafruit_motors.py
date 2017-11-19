'''
    Adafruit DC HAT implementation for Motors
'''
try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT
except:
    print('Adafruit Motor HAT lib is not available')

from .motors import Motors

class AdafruitMotors(Motors):
    '''
        Motors implementation for the Adafruit DC & Stepper HAT
    '''
    def __init__(self, addr=0x60, left_id=2, right_id=1):
        Motors.__init__(self)

        # Start at ~30% speed
        self.speed = 85

        # Speed values are 0 - 255
        self.max_speed = 255

        # We need to make the motors stateful
        # They don't seem to deal well with quick on/off actions
        self.power_left = 0
        self.power_right = 0

        self.speed_changed = False

        if self.running_on_pi:
            import atexit

            # default I2C address is 0x60
            self.motors = Adafruit_MotorHAT(addr)

            self.left_motor = self.motors.getMotor(left_id)
            self.right_motor = self.motors.getMotor(right_id)

            # Start with motors turned off.
            self.left_motor.run(Adafruit_MotorHAT.RELEASE)
            self.right_motor.run(Adafruit_MotorHAT.RELEASE)

            # Configure all motors to stop at program exit if desired.
            atexit.register(self.stop)
        else:
            self.motors = None

    def control_motors(self, power_left, power_right):
        if self.running_on_pi:
            if power_left == power_right == 0:
                return self.stop()

            if self.power_left != power_left or self.speed_changed:
                # Adjust left motor if we have to
                self.power_left = power_left
                self.left_motor.setSpeed(int(float(abs(power_left)) / 100.0 * self.speed))
                self.left_motor.run(
                    Adafruit_MotorHAT.FORWARD if power_left >= 0 else Adafruit_MotorHAT.BACKWARD)

            if self.power_right != power_right or self.speed_changed:
                # Same for right motor
                self.power_right = power_right
                self.right_motor.setSpeed(int(float(abs(power_right)) / 100.0 * self.speed))
                self.right_motor.run(
                    Adafruit_MotorHAT.FORWARD if power_right >= 0 else Adafruit_MotorHAT.BACKWARD)

            # Reset flag
            self.speed_changed = False

    def set_speed(self, speed):
        '''
            Set speed to a given amount
        '''
        Motors.set_speed(self, speed)
        self.speed_changed = True

    def stop(self):
        if self.running_on_pi:
            # Kill power
            self.power_left = self.power_right = 0

            self.left_motor.run(Adafruit_MotorHAT.RELEASE)
            self.right_motor.run(Adafruit_MotorHAT.RELEASE)
