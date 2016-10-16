# Hack to find the local keyboard module
from sys import path
path.insert(0, '../lib/keyboard/')

from keyboard import keyboard

from r_server.robot_server import Directions

class KeyboardController:
	'''Implements direct control using a connected USB keyboard'''
	def __init__(self, robot):
		self.robot = robot

		# Press PAGE UP then PAGE DOWN to type "foobar".
		self.wHook = keyboard.hook_key('w', lambda: robot.move(Directions.Forward), lambda: robot.stop(Directions.Forward))
		#self.sHook = keyboard.add_hotkey('s', lambda: robot.move(Directions.Back))
		#self.aHook = keyboard.add_hotkey('a', lambda: robot.move(Directions.Left))
		#self.dHook = keyboard.add_hotkey('d', lambda: robot.move(Directions.Right))
	def halt(self):
		keyboard.listener.remove_handler(self.wHook)
		#keyboard.remove_hotkey('s')
		#keyboard.remove_hotkey('a')
		#keyboard.remove_hotkey('s')
		#keyboard.remove_hotkey('d')
		pass



		


