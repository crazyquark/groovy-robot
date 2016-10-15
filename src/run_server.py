#!/usr/bin/env python
'''
	Run the server
'''

from r_server import bottle_server
from keyboard_controller import KeyboardController
import sys

keyboardController = KeyboardController(bottle_server.getRobotServer())

try:
	bottle_server.run()
except:
	bottle_server.halt()
	keyboardController.halt()

	sys.exit(0)