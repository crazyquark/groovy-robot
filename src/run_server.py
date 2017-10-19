#!/usr/bin/env python
'''
    Run the server
'''

from r_server import web_server
from r_server.robot_server import RobotServer
from camera_server.camera_server import CameraServer

import sys, traceback

import signal
import sys

enableKeyboard = False
try:
    from keyboard_controller import KeyboardController
except:
    print 'Keyboard error: probably there is no keyboard connected, disabling'
    print 'Cause might be: '
    traceback.print_exc()

    enableKeyboard = False

def haltHandler(*_):
    camera.halt()
    web_server.halt()
    if enableKeyboard:
        keyboardController.halt()
        sys.exit(0)

signal.signal(signal.SIGINT, haltHandler)
signal.signal(signal.SIGTERM, haltHandler)

try:
    robot = RobotServer()

    # Camera, lights, action!
    camera = CameraServer()

    if enableKeyboard:
        keyboardController = KeyboardController(robot)

    web_server.run(robot, camera)
except:
    print 'Caught a bogie: '
    traceback.print_exc()

    haltHandler()

    print 'There was an error, halting...'
    sys.exit(0)
