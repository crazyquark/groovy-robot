import Adafruit_PCA9685

class ServoMotor:
    '''
        Controls a servo motor on one of the PCA9685's channels
        Based on: https://rootsaid.com/pca9685-servo-driver/
    '''

    min_pulse_width = 650
    max_pulse_width = 2350
    default_pulse_width = 1500

    def __init__(self, channel=0, addr=0x60, frequency=60):
        # Warning: setting the frequency breaks any other PWM control on this chip
        # Don't control multiple things at once
        self.addr = addr
        self.frequency = frequency
        self.channel = channel

        self.pwm = None

    def __enter__(self):
        self.activate()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deactivate()

    def pulse_width(self, angle):
        angle_to_pulse = ((angle * (ServoMotor.max_pulse_width -
                                    ServoMotor.min_pulse_width)) / 180) + ServoMotor.min_pulse_width
        analog_value = int(float(angle_to_pulse) / 1000000 * self.frequency * 4096)

        print('servo:', analog_value)

        return analog_value

    def activate(self):
        '''
        Activates this servo; always do this first
        '''
        if not self.pwm:
            self.pwm = Adafruit_PCA9685.PCA9685(address=self.addr)
            self.pwm.setPWMFreq(self.frequency)
            self.pwm.setPWM(self.channel, 4096, 0)

    def deactivate(self, old_freq = 1600):
        '''
        Deactivates this servo; always deativate after use!
        '''
        if self.pwm:
            # set to off
            self.pwm.setPWM(self.channel, 0, 4096)
            self.pwm.setPWMFreq(old_freq)
            del self.pwm
            self.pwm = None

    def rotate(self, angle):
        if self.pwm:
            self.pwm.setPWM(self.channel, 0, self.pulse_width(angle))

if __name__ == '__main__':
    print('Running servo test')
    with ServoMotor() as servo:
        servo.rotate(100)