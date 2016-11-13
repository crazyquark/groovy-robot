# Hack to find the local keyboard module
from sys import path
path.insert(0, '../lib/keyboard/')

import keyboard

from r_server.robot_server import Directions, Throttle

# These seem to be different on Linux
ARROW_UP = 103
ARROW_DOWN = 108
ARROW_LEFT = 105
ARROW_RIGHT = 106

class KeyboardController:
	'''Implements direct control using a connected USB keyboard'''
	def __init__(self, robot):
		# Press PAGE UP then PAGE DOWN to type "foobar".
		self.hooks = []
		#TODO: use a single handler for all keys
		self.hooks.append(keyboard.hook_key('w', lambda: robot.move(Directions.Forward), lambda: robot.stop(Directions.Forward)))
		self.hooks.append(keyboard.hook_key(ARROW_UP, lambda: robot.move(Directions.Forward), lambda: robot.stop(Directions.Forward)))

		self.hooks.append(keyboard.hook_key('s', lambda: robot.move(Directions.Back), lambda: robot.stop(Directions.Back)))
		self.hooks.append(keyboard.hook_key(ARROW_DOWN, lambda: robot.move(Directions.Back), lambda: robot.stop(Directions.Back)))

		self.hooks.append(keyboard.hook_key('a', lambda: robot.move(Directions.Left), lambda: robot.stop(Directions.Left)))
		self.hooks.append(keyboard.hook_key(ARROW_LEFT, lambda: robot.move(Directions.Left), lambda: robot.stop(Directions.Left)))

		self.hooks.append(keyboard.hook_key('d', lambda: robot.move(Directions.Right), lambda: robot.stop(Directions.Right)))
		self.hooks.append(keyboard.hook_key(ARROW_RIGHT, lambda: robot.move(Directions.Right), lambda: robot.stop(Directions.Right)))
		
		self.hooks.append(keyboard.hook_key('z', lambda: robot.speedAdjust(Throttle.Down), lambda: None))
		self.hooks.append(keyboard.hook_key('x', lambda: robot.speedAdjust(Throttle.Up), lambda: None))
	def halt(self):
		for hook in self.hooks:
			try:
				keyboard.listener.remove_handler(hook)
			except:
				print 'Failed to remove hook: ' + str(hook)


		


