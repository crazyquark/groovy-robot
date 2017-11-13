'''
    Motor drivers available: Adafruit DC Motors Hat and GrovePi motor module
'''

class Motors(object):
    '''
        Generic motors implementation
    '''
    def __init__(self):
        self.speed = 0

        # Default speed values: 0 - 100
        self.max_speed = 100

        from platform import uname
        self.running_on_pi = uname()[4].startswith('arm')

    def change_speed(self, amount):
        '''
            Increase/decrease speed
        '''
        self.speed += amount

        if self.speed <= 0:
            self.speed = 0
            return
        
        self.speed = min(self.speed, self.max_speed)
        

        print('SPEED: ' + str(self.speed))

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
