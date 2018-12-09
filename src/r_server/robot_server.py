'''
    Robot Server
'''
import platform
import traceback
from subprocess import Popen, PIPE
from time import sleep, time
import os

import RPi.GPIO as GPIO

from debug.debuggable_process import DebuggableProcess
from display.oled_display import OledDisplay

from motors.adafruit_motors import AdafruitMotors
from motors.stepper_motor import StepperMotor


class Directions(object):
    '''
        Simple enumeration of the available directions
    '''
    Start, Forward, Back, Left, Right, End = range(1, 7)


class CameraMovement(object):
    '''
        Enumeration of camera directions
    '''
    Up, Down, Idle = [1, -1, 0]


class Throttle(object):
    '''
        Simple enumerations of the directions signs: up or down
    '''
    Up, Down = (1, -1)


class RobotServer(DebuggableProcess):
    '''
        Server component for controlling a local GrovePi based robot
        Uses an autostart thread to run its update loop
    '''

    def __init__(self, queue):
        self.queue = queue

        self.fwd_pressed = False
        self.back_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.turn_factor = 2  # controls how sharp the turns will be

        # How much to increase speed at one time
        self.speed_increment = 5

        # Check if this is the real deal
        arch = platform.uname()[4]
        self.running_on_pi = True if arch.startswith('arm') else False

        print('We are running on: ', arch)

        # self.setupBatterySafeStop()

        # Camera control
        self.camera_state = 0

        # Adjust for veering left
        self.motors = AdafruitMotors(right_trim=-10)
        self.camera_stepper = StepperMotor(self.motors)

        super(RobotServer, self).__init__()

        self.manual = False
        self.manual_mode_left_power = 0
        self.manual_mode_right_power = 0
        self.running = True
        self.start()

    def setupBatterySafeStop(self):
        def shutdown(_):
            pass
            #print('Low battery detected, shutting down now!')
            # self.halt()
            #os.system('sudo shutdown -h now')

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.IN)

        status = GPIO.input(16)
        if (status == 0):
            # we are running in battery free mode
            return

        GPIO.add_event_detect(16, GPIO.FALLING)
        GPIO.add_event_callback(16, shutdown)

    def tilt_camera(self, dir):
        self.camera_state = dir

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
        self.display = OledDisplay()
        self.last_update = 0

        while self.running:
            try:
                self.get_sbc_status()

                # Camera stepper control
                if self.camera_state != CameraMovement.Idle:
                    # Tilt camera up or down
                    self.camera_stepper.step(self.camera_state)
                else:
                    self.camera_stepper.stop()

                message = self.queue.get()
                self.process_message(message)

                # DC motors control
                if self.manual:
                    self.motors.control_motors(
                        self.manual_mode_left_power, self.manual_mode_right_power)
                else:
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
                        self.motors.control_motors(
                            sign * 100, sign * 100 / self.turn_factor)
                    elif (self.fwd_pressed or self.back_pressed) and self.left_pressed:
                        # Attempt to turn left
                        sign = 1 if self.fwd_pressed else -1
                        self.motors.control_motors(
                            sign * 100 / self.turn_factor, sign * 100)
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

    def process_message(self, message):
        if message > Directions.Start and message < Directions.End:
            self.process_press(message)

    def process_press(self, direction):
        '''
            Interpret a key press from UI or a controller that requires continous movements
        '''
        if direction == Directions.Forward:
            self.fwd_pressed = not self.fwd_pressed
        elif direction == Directions.Back:
            self.back_pressed = not self.back_pressed
        elif direction == Directions.Left:
            self.left_pressed = not self.left_pressed
        elif direction == Directions.Right:
            self.right_pressed = not self.right_pressed

    def move(self, direction):
        '''
            Move robot
        '''
        if not self.running_on_pi:
            return

        self.process_press(direction)

    def stop(self, direction):
        '''
            Full stop
        '''
        if not self.running_on_pi:
            return

        self.process_press(direction)

    def manual_mode(self, enable):
        '''
            Enable or disable manual mode
        '''
        self.manual = enable

    def set_motors(self, left_power, right_power):
        '''
            In manual mode set the motors power directly
        '''
        if not self.manual:
            return  # only available in manual mode

        self.manual_mode_left_power = min(100, max(-100, left_power))
        self.manual_mode_right_power = min(100, max(-100, right_power))

    def get_sbc_status(self):
        # Update every 5 seconds
        now = time()
        if now - self.last_update > 5:
            self.last_update = now
            self.display.set_text([])

            temp = 0
            freqs = [0 for i in range(0, 4)]
            with open('/sys/class/thermal/thermal_zone0/temp') as fd:
                temp = int(int(fd.read()) / 1000)

                color = 'red' if temp > 80 else 'blue'
                self.display.append_text(
                    ' T: ' + str(temp) + '°C', color)

            for i in range(0, 4):
                with open('/sys/devices/system/cpu/cpu' + str(i) + '/cpufreq/scaling_cur_freq') as fd:
                    freqs[i] = int(int(fd.read()) / 1000)
                    self.display.append_text(
                        'CPU' + str(i) + ':' + str(freqs[i]) + 'MHz', 'purple')

            self.display.set_refresh(True)

    def halt(self):
        '''
            Stop main loop
        '''
        self.running = False
        self.motors.stop()
        self.camera_stepper.stop()
