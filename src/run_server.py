#!/usr/bin/env python
'''
	Run the server
'''

from r_server import bottle_server
import sys, traceback

enableKeyboard = True
try:
	from keyboard_controller import KeyboardController
except:
	print 'Keyboard error: probably there is no keyboard connected, disabling'
	print 'Cause might be: '
	traceback.print_exc()

	enableKeyboard = False

if enableKeyboard:
	keyboardController = KeyboardController(bottle_server.getRobotServer())

try:
	bottle_server.run()
except:
	bottle_server.halt()
	#keyboardController.halt()

	sys.exit(0)