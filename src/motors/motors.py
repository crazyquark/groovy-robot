'''
    Motor drivers available: Adafruit DC Motors Hat and GrovePi motor module
'''

class Motors(object):
    '''
        Generic motors implementation
    '''
    def __init__(self, running_on_arm, left_trim=0, right_trim=0):
        self.speed = 0

        # for uneven motors, we need to trim
        self.left_trim = left_trim
        self.right_trim = right_trim

        # Default speed values: 0 - 100
        self.max_speed = 100

        self.running_on_arm = running_on_arm

    def change_speed(self, amount):
        '''
            Increase/decrease speed
        '''
        self.speed += amount

        if self.speed <= 0:
            self.speed = 0
            return

        old_speed = self.speed
        self.speed = min(self.speed, self.max_speed)
        self.speed_changed = old_speed != self.speed

        print('SPEED: ' + str(self.speed))

    def set_speed(self, speed):
        '''
            Set speed to a given amount
        '''
        self.speed = min(speed, self.max_speed)

    def control_motors(self, left_power, right_power):
        '''
            Control the 2 motors independetly by applying a power factor
        '''
        if not self.running_on_arm:
            return

    def stop(self):
        '''
            Emergency stop
        '''
        self.speed = 0
