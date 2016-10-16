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

try:
	if enableKeyboard:
		keyboardController = KeyboardController(bottle_server.getRobotServer())
	bottle_server.run()
except:
	traceback.print_exc()

	bottle_server.halt()
	if enableKeyboard:
		keyboardController.halt()
	
	print 'There was an error, halting...'
	sys.exit(0)