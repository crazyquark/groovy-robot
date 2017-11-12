from threading import Thread
from .robot_server import Directions, Throttle

try:
    import evdev
    EVDEV_AVAILABLE = True
except ImportError:
    print('evdev is not available')
    EVDEV_AVAILABLE = False

class PS3Controller(Thread):
    '''
        Connects to any available PS3 controller and reads events
    '''
    def __init__(self, robot):
        if not EVDEV_AVAILABLE:
            print('No evdev, no joy, exiting...')
            return

        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        for dev in devices:
            if dev.name == 'Sony Computer Entertainment Wireless Controller':
                self.device = dev
                break
        if not self.device:
            print('Failed to detect sixaxis controller!')

        Thread.__init__(self)

        self.robot = robot
        self.running = True
        self.start()

    def run(self):
        if not self.device:
            print('No controller connected, existing')
            return

        for event in self.device.read_loop():
            if not self.running:
                return

            self.process_event(event)

    def process_event(self, event):
        '''
            Executs action based on button presses
        '''
        if event.type == 1: # key press
            if event.code == 297:
                self.robot.move(Directions.Forward)
        else:
            self.robot.halt()


    def halt(self):
        '''
            Stops thread
        '''
        self.running = False
