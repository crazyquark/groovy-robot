#!/usr/bin/env python

import time
import signal
import sys
import pygame

# VS Debug support
from ptvsd import enable_attach as enableAttach
enableAttach('kriekpi') 

from motors.adafruit_motors import AdafruitMotors

class Robot:
    def __init__(self):
        # pygame.init()


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
            self.motors = AdafruitMotors()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_d:
                            self.motors.control_motors(100, -50)
                        elif event.key == pygame.K_a:
                            self.motors.control_motors(-50, 100)
                        elif event.key == pygame.K_w:
                            self.motors.control_motors(100, 100)
                        elif event.key == pygame.K_s:
                            self.motors.control_motors(-100, -100)
                        elif event.key == pygame.K_z:
                            self.motors.change_speed(+5)
                        elif event.key == pygame.K_x:
                            self.motors.change_speed(-5)
                    elif event.type == pygame.KEYUP:
                        self.motors.stop()
        except IOError as e:
            print('Unable to find the motor driver, check the address and press reset on the motor driver and try again')
            print('I/O error({0}): {1}'.format(e.errno, e.strerror))

if __name__ == '__main__':
    robbie = Robot()