#!/usr/bin/env python
'''
	Run the server
'''

from r_server import bottle_server
from r_server.robot_server import RobotServer
from camera_server.camera import Camera

import sys, traceback

import signal
import sys




enableKeyboard = True
try:
	from keyboard_controller import KeyboardController
except:
	print 'Keyboard error: probably there is no keyboard connected, disabling'
	print 'Cause might be: '
	traceback.print_exc()

	enableKeyboard = False

def haltHandler(*_):
	camera.halt()
	bottle_server.halt()
	if enableKeyboard:
		keyboardController.halt()
		sys.exit(0)

signal.signal(signal.SIGINT, haltHandler)
signal.signal(signal.SIGTERM, haltHandler)

try:
	robot = RobotServer()

	# Camera, lights, action!
	camera = Camera()
	camera.start()

	if enableKeyboard:
		keyboardController = KeyboardController(robot)

	bottle_server.run(robot)
except:
	print 'Caught a bogie: '
	traceback.print_exc()
	
	haltHandler()
	
	print 'There was an error, halting...'
	sys.exit(0)