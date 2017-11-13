'''
    Robot Server
'''
import platform
import traceback
from threading import Thread, Condition
from time import sleep

from motors.adafruit_motors import AdafruitMotors

class Directions(object):
    '''
        Simple enumeration of the available directions
    '''
    Forward, Back, Left, Right = range(4)

class Throttle(object):
    '''
        Simple enumerations of the directions signs: up or down
    '''
    Up, Down = (1, -1)

class RobotServer(Thread):
    '''
        Server component for controlling a local GrovePi based robot
        Uses an autostart thread to run its update loop
    '''
    def __init__(self):
        self.fwd_pressed = False
        self.back_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.turn_factor = 2 # controls how sharp the turns will be

        # How much to increase speed at one time
        self.speed_increment = 5

        # Check if this is the real deal
        arch = platform.uname()[4]
        self.running_on_pi = True if arch.startswith('arm') else False

        print('We are running on: ', arch)

        self.motors = AdafruitMotors()

        Thread.__init__(self)
        self.manual = False
        self.condition = Condition()
        self.running = True
        self.start()

    def no_key_pressed(self):
        '''
            Check the no keys pressed condition
        '''
        return not self.fwd_pressed and not self.back_pressed and \
            not self.left_pressed and not self.right_pressed

    def bad_key_combo(self):
        '''
            Check if both fowd and reverse are pressed or both left and right are pressed
        '''
        return (self.fwd_pressed and self.back_pressed) or \
            (self.left_pressed and self.right_pressed)

    def run(self):
        while self.running:
            # Processing is suspended
            if self.manual:
                self.condition.acquire()
                self.condition.wait()
                self.condition.release()

            try:
                if self.no_key_pressed() or self.bad_key_combo():
                    # Full stop
                    self.motors.stop()
                elif not self.left_pressed and not self.right_pressed and self.fwd_pressed:
                    # Full steam ahead!
                    self.motors.control_motors(100, 100)
                elif not self.left_pressed and not self.right_pressed and self.back_pressed:
                    # All engines reverse!
                    self.motors.control_motors(-100, -100)
                elif not self.back_pressed and not self.fwd_pressed and self.right_pressed:
                    # In place right turn
                    self.motors.control_motors(100, -100)
                elif not self.back_pressed and not self.fwd_pressed and self.left_pressed:
                    # In place left turn
                    self.motors.control_motors(-100, 100)
                elif (self.fwd_pressed or self.back_pressed) and self.right_pressed:
                    # Attempt to turn right
                    sign = 1 if self.fwd_pressed else -1
                    self.motors.control_motors(sign * 100, sign * 100 / self.turn_factor)
                elif (self.fwd_pressed or self.back_pressed) and self.left_pressed:
                    # Attempt to turn left
                    sign = 1 if self.fwd_pressed else -1
                    self.motors.control_motors(sign * 100 / self.turn_factor, sign * 100)
                else:
                    # I donno
                    self.motors.control_motors(0, 0)
            except:
                print('Critical failure, shutting down')
                print('Possible cause: ')
                traceback.print_exc()
                self.running = False
                raise Exception('Motors failure')

    def speed_adjust(self, direction):
        '''
            Increase or decrease speed depending on the sign of direction
        '''
        if self.running_on_pi:
            amount = direction * self.speed_increment
            self.motors.change_speed(amount)

    def set_speed(self, speed):
        '''
            Sets speed to a specific value
        '''
        if self.running_on_pi:
            self.motors.set_speed(speed)

    def process_press(self, direction, is_on):
        '''
            Interpret a key press from UI or a controller that requires continous movements
        '''
        if direction == Directions.Forward:
            self.fwd_pressed = is_on
        elif direction == Directions.Back:
            self.back_pressed = is_on
        elif direction == Directions.Left:
            self.left_pressed = is_on
        elif direction == Directions.Right:
            self.right_pressed = is_on

    def move(self, direction):
        '''
            Move robot
        '''
        print('MOVE: ', direction)

        if not self.running_on_pi:
            return

        self.process_press(direction, True)

    def stop(self, direction):
        '''
            Full stop
        '''
        print('STOP: ', direction)

        if not self.running_on_pi:
            return

        self.process_press(direction, False)

    def manual_mode(self, enable):
        '''
            Enable or disable manual mode
        '''
        self.manual = enable
        if not self.manual:
            self.condition.acquire()
            self.condition.notify()
            self.condition.release()

    def set_motors(self, left_power, right_power):
        '''
            In manual mode set the motors power directly
        '''
        if not self.manual:
            return # only available in manual mode

        self.motors.control_motors(min(100, max(-100, left_power)),
                                   min(100, max(-100, right_power)))

    def halt(self):
        '''
            Stop main loop
        '''
        self.running = False
        