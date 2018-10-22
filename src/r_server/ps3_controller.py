from threading import Thread
from time import sleep
from .robot_server import Directions, Throttle, CameraMovement

try:
    import evdev
    EVDEV_AVAILABLE = True
except ImportError:
    print('evdev is not available')
    EVDEV_AVAILABLE = False


class SixAxisButtonCodes:
    '''
        Enum to map PS3 evdev button codes
    '''
    Select = 314
    Start = 315
    Cross = 304
    Circle = 305
    Triangle = 307
    Square = 308
    R1 = 311
    R2 = 313
    R3 = 318
    L1 = 310
    L2 = 312
    L3 = 317
    DPadUp = 544
    DPadDown = 545
    DPadLeft = 546
    DPadRight = 547


class PS3Controller(Thread):
    '''
        Connects to any available PS3 controller and reads events
        Inspired by http://www.ev3dev.org/docs/tutorials/using-ps3-sixaxis/
    '''

    def __init__(self, robot):
        if not EVDEV_AVAILABLE:
            print('No evdev, no joy, exiting...')
            return

        self.device = None
        self.detect_controller()

        super(PS3Controller, self).__init__()

        self.robot = robot
        self.running = True
        self.start()

    def detect_controller(self):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for dev in devices:
            if dev.name == 'Sony Computer Entertainment Wireless Controller':
                self.device = dev
                break

    def run(self):
        while not self.device:
            self.detect_controller()
            sleep(5)

        for event in self.device.read_loop():
            if not self.running:
                return

            self.process_event(event)

    def process_event(self, event):
        '''
            Executs action based on button presses
        '''
        self.simple_mode_process(event)

    def tank_mode_process(self, event):
        if event.type == 3:
            if event.code == 48:
                self.tank_mode_left_power = event.value
            elif event.code == 49:
                self.tank_mode_right_power = event.value

            # Adjust motors manually
            self.robot.set_motors(self.tank_mode_left_power, self.tank_mode_right_power)

    def game_mode_process(self, event):
        '''
            More advanced control mode that use the analog input from the triggers to control speed
        '''
        if event.type == 3: # analog event
            if event.code == 48:
                # left trigger
                self.robot.set_speed(event.value)
                self.robot.process_press(Directions.Back, event.value > 0)
            elif event.code == 49:
                # right trigger
                self.robot.set_speed(event.value) # [0, 255]
                self.robot.process_press(Directions.Forward, event.value > 0)
            elif event.code == 0: # left thumbstick
                if event.value < 50:
                    self.robot.process_press(Directions.Left, True)
                elif event.value > 50 and event.value <= 128:
                    self.robot.process_press(Directions.Left, False)
                elif event.value > 178:
                    self.robot.process_press(Directions.Right, True)
                elif event.value > 128 and event.value < 178:
                    self.robot.process_press(Directions.Right, False)
        elif event.type == 1:
            # D-Pad
            if event.code == 295:
                self.robot.process_press(Directions.Left, event.value == 1)
            elif event.code == 293:
                self.robot.process_press(Directions.Right, event.value == 1)

    def simple_mode_process(self, event):
        '''
            A simplistic control scheme which uses only the shoulder buttons
            as digital inputs
        '''
        if event.type == 1: # key press
            if event.code == SixAxisButtonCodes.R2:
                if event.value == 1:
                    self.robot.move(Directions.Forward)
                else:
                    self.robot.stop(Directions.Forward)
            elif event.code == SixAxisButtonCodes.L2:
                if event.value == 1:
                    self.robot.move(Directions.Back)
                else:
                    self.robot.stop(Directions.Back)
            elif event.code == SixAxisButtonCodes.L1:
                if event.value == 1:
                    self.robot.move(Directions.Left)
                else:
                    self.robot.stop(Directions.Left)
            elif event.code == SixAxisButtonCodes.R1:
                if event.value == 1:
                    self.robot.move(Directions.Right)
                else:
                    self.robot.stop(Directions.Right)
            elif event.code == SixAxisButtonCodes.R3:
                if event.value == 1:
                    self.robot.tilt_camera(CameraMovement.Up)
                else:
                    self.robot.tilt_camera(CameraMovement.Idle)
            elif event.code == SixAxisButtonCodes.L3:
                if event.value == 1:
                    self.robot.tilt_camera(CameraMovement.Down)
                else:
                    self.robot.tilt_camera(CameraMovement.Idle)

    def halt(self):
        '''
            Stops thread
        '''
        self.running = False
