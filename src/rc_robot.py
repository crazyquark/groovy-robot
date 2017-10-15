#!/usr/bin/env python

import time
import signal
import sys
import pygame

# VS Debug support
from ptvsd import enable_attach as enableAttach
enableAttach('kriekpi') 

# Check if we're on an RPi
runningOnPi = True
try:
    from grovepi_driver.grove_i2c_motor_driver import motor_driver as motorDriver
except:
    runningOnPi = False

class Robot:
    def __init__(self):
        pygame.init();

        # Directions
        # '0b1010' defines the output polarity, '10' means the M+ is 'positive' while the M- is 'negative'
        self.forwardDir  = 0b0101
        self.backwardDir = 0b1010
        self.leftDir	 = 0b1001
        self.rightDir	 = 0b0110

        # Attempting to limit max speed to avoid crashes
        self.maxSpeed = 95

        wallEpic = pygame.image.load('res/wall-e-800.jpg')
        self.screen = pygame.display.set_mode(wallEpic.get_rect().size)

        self.screen.blit(wallEpic, (0,0))
        pygame.display.flip()

        signal.signal(signal.SIGINT, self.signalHandler)

        self.speed = 75 # 75%, let's save battery power
        self.setupMotors()

    def signalHandler(self, smth, another):
        print('Bye!')
        sys.exit(0)

    def setupMotors(self):
        try:
            # You can initialize with a different address too: grove_i2c_motor_driver.motor_driver(address=0x0a)
            if runningOnPi:
                m = motorDriver()
            else:
                m = ''

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            self.left(m)
                        elif event.key == pygame.K_d:
                            self.right(m)
                        elif event.key == pygame.K_w:
                            self.forward(m)
                        elif event.key == pygame.K_s:
                            self.backward(m)
                        elif event.key == pygame.K_z:
                            self.speedAdjust(+5)
                        elif event.key == pygame.K_x:
                            self.speedAdjust(-5)
                    elif event.type == pygame.KEYUP:
                        self.stop(m)
        except IOError as e:
            print('Unable to find the motor driver, check the address and press reset on the motor driver and try again')
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))
    
    def speedAdjust(self, amount):
        print('SPEED: ' + str(amount))
        self.speed += amount

        if self.speed >= self.maxSpeed:
            self.speed = self.maxSpeed
        elif self.speed <= 0:
            self.speed = 0

    def left(self, m):
        print('LEFT')

        if not runningOnPi:
            return

        m.MotorSpeedSetAB(self.speed,self.speed)
        m.MotorDirectionSet(self.leftDir)
    
    def right(self, m):
        print('RIGHT')

        if not runningOnPi:
            return

        m.MotorSpeedSetAB(self.speed,self.speed)	
        m.MotorDirectionSet(self.rightDir)

    def forward(self, m):
        print('FORWARD')

        if not runningOnPi:
            return

        m.MotorSpeedSetAB(self.speed,self.speed)	
        m.MotorDirectionSet(self.forwardDir)	

    def backward(self, m):
        print('BACKWARD')

        if not runningOnPi:
            return

        m.MotorSpeedSetAB(self.speed,self.speed)	
        m.MotorDirectionSet(self.backwardDir)	

    def stop(self, m):
        print('STOP')

        if not runningOnPi:
            return

        m.MotorSpeedSetAB(0,0)

if __name__ == '__main__':
    robbie = Robot()