from threading import Thread
from .robot_server import Directions, Throttle

try:
    import evdev
    EVDEV_AVAILABLE = True
except ImportError:
    print('evdev is not available')
    EVDEV_AVAILABLE = False

class ControlScheme(object):
    '''
        Simple enumeration of the available control schemes
    '''
    SimpleMode, GameMode, TankMode, NumSchemes = range(4)

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
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for dev in devices:
            if dev.name == 'Sony Computer Entertainment Wireless Controller':
                self.device = dev
                break
        if not self.device:
            print('Failed to detect sixaxis controller!')

        Thread.__init__(self)

        self.control_scheme = ControlScheme.SimpleMode

        # Used for tank mode
        self.current_direction = Directions.Forward

        self.robot = robot
        self.running = True
        self.start()

        self.tank_mode_left_power = 0
        self.tank_mode_right_power = 0

    def run(self):
        if not self.device:
            print('No controller connected, existing')
            return

        for event in self.device.read_loop():
            if not self.running:
                return

            self.process_event(event)

    def switch_scheme(self):
        '''
            Changes control scheme
        '''
        self.control_scheme += 1
        if self.control_scheme == ControlScheme.NumSchemes:
            self.control_scheme = 0

        if self.control_scheme == ControlScheme.SimpleMode:
            self.robot.set_speed(85) # reset speed

        self.robot.manual_mode(self.control_scheme == ControlScheme.TankMode)

        print('Control scheme switched to: ', str(self.control_scheme))

    def process_event(self, event):
        '''
            Executs action based on button presses
        '''
        if event.type == 1 and event.code == 288 and event.value == 1:
            # Select changes control scheme
            self.switch_scheme()
        else:
            if self.control_scheme == ControlScheme.SimpleMode:
                self.simple_mode_process(event)
            elif self.control_scheme == ControlScheme.GameMode:
                self.game_mode_process(event)
            elif self.control_scheme == ControlScheme.TankMode:
                self.tank_mode_process(event)

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
            if event.code == 297:
                if event.value == 1:
                    self.robot.move(Directions.Forward)
                else:
                    self.robot.stop(Directions.Forward)
            elif event.code == 296:
                if event.value == 1:
                    self.robot.move(Directions.Back)
                else:
                    self.robot.stop(Directions.Back)
            elif event.code == 298:
                if event.value == 1:
                    self.robot.move(Directions.Left)
                else:
                    self.robot.stop(Directions.Left)
            elif event.code == 299:
                if event.value == 1:
                    self.robot.move(Directions.Right)
                else:
                    self.robot.stop(Directions.Right)

    def halt(self):
        '''
            Stops thread
        '''
        self.running = False
