try:
    from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
except:
    print('Stepper motor not available, probably not running on a Pi')

from platform import uname

class StepperMotor:
    '''
        See https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors
    '''
    def __init__(self, adafruit_motors):
        self.running_on_pi = uname()[4].startswith('arm')
        if self.running_on_pi:
            self.motors = adafruit_motors.motors

            self.stepper = self.motors.getStepper(35, 2) # 200 steps/rev, motor port #2
            # self.stepper.setSpeed(30)                  # 30 RPM
    
    def step(self, dir):
        if not self.running_on_pi:
            return

        direction = Adafruit_MotorHAT.FORWARD if dir > 0 else Adafruit_MotorHAT.BACKWARD
        self.stepper.oneStep(direction, Adafruit_MotorHAT.SINGLE)

    def stop(self):
        if not self.running_on_pi:
            return
        
        # stop M3 and M4
        self.motors.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.motors.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
