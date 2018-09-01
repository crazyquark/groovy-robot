try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
except:
    print('Stepper motor not available, probably not running on a Pi')

from math import fabs
from platform import uname

class StepperMotor:
    def __init__(self, adafruit_motors):
        self.running_on_pi = uname()[4].startswith('arm')
        if self.running_on_pi:
            self.motors = adafruit_motors

            self.stepper = self.motors.getStepper(200, 2) # 200 steps/rev, motor port #2
            self.stepper.setSpeed(60)                     # 60 RPM
    
    def rotate(self, steps):
        if not self.running_on_pi:
            return

        direction = Adafruit_MotorHAT.FORWARD if steps > 0 else Adafruit_MotorHAT.BACKWARD
        self.stepper(direction, Adafruit_MotorHAT.DOUBLE)

    def stop(self):
        if not self.running_on_pi:
            return
        
        # stop M3 and M4
        self.motors.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.motors.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
