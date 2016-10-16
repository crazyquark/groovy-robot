#!/usr/bin/env python
'''
	Run the server
'''

from r_server import bottle_server
import sys

enableKeyboard = True
try:
	from keyboard_controller import KeyboardController
except e:
	print 'Keyboard error: probably there is no keyboard connected, disabling'
	print 'Error is ' + e
	enableKeyboard = False

if enableKeyboard:
	keyboardController = KeyboardController(bottle_server.getRobotServer())

try:
	bottle_server.run()
except:
	bottle_server.halt()
	#keyboardController.halt()

	sys.exit(0)