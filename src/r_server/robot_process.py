'''
    Robot Server
'''
import traceback
from subprocess import Popen, PIPE
from time import sleep
from multiprocessing import Queue
import os

# from display.oled_display import OledDisplay
from debug.debuggable_process import DebuggableProcess
from controllers.ps3_controller import PS3Controller

from motors.adafruit_motors import AdafruitMotors, StepperDirections

from controllers.enums import Directions, Throttle, CameraMovement


class RobotProcess(DebuggableProcess):
    '''
        Robot process
    '''

    def __init__(self, queue, running_on_arm):
        self.running_on_arm = running_on_arm
        
        self.queue = queue

        self.fwd_pressed = False
        self.back_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.turn_factor = 2  # controls how sharp the turns will be

        # How much to increase speed at one time
        self.speed_increment = 5

        # self.setupBatterySafeStop()

        # Camera control
        self.camera_state = 0

        # Adjust for veering left
        self.motors = AdafruitMotors(running_on_arm = self.running_on_arm)

        super(RobotProcess, self).__init__()

        self.manual = False
        self.manual_mode_left_power = 0
        self.manual_mode_right_power = 0
        self.running = True

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
        self.enable_debug(7878)
        self.enable_logging('robot')

        # self.display = OledDisplay() if self.running_on_arm else None
        self.last_update = 0

        while self.running:
            try:
                # self.get_sbc_status()
                # Camera stepper control
                # if self.camera_state != CameraMovement.Idle:
                #     # Tilt camera up or down
                #     self.motors.step(StepperDirections.Forward if self.camera_state == CameraMovement.Up else StepperDirections.Backward)
                try:
                    if (not self.queue.empty()):
                        message = self.queue.get_nowait()
                        self.process_message(message)
                except Exception as ex:
                    print(ex)
                    continue

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
            except Exception:
                print('Motors error, attempting to recover')
                traceback.print_exc()
                self.motors.stop()
                continue

    def speed_adjust(self, direction):
        '''
            Increase or decrease speed depending on the sign of direction
        '''
        if self.running_on_arm:
            amount = direction * self.speed_increment
            self.motors.change_speed(amount)

    def set_speed(self, speed):
        '''
            Sets speed to a specific value
        '''
        if self.running_on_arm:
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
        if not self.running_on_arm:
            return

        self.process_press(direction)

    def stop(self, direction):
        '''
            Full stop
        '''
        if not self.running_on_arm:
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
        if not self.running_on_arm:
            return

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

    @classmethod
    def start_robot(cls, running_on_arm):
        if hasattr(cls, 'instance'):
            return cls.queue

        cls.queue = Queue(5)
        cls.instance = RobotProcess(cls.queue, running_on_arm)
        cls.instance.start()

        return cls.queue

    @classmethod
    def stop_robot(cls):
        if hasattr(cls, 'instance'):
            cls.instance.halt()
            cls.instance.terminate()
