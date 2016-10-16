import keyboard
from keyboard.keyboard_event import normalize_name, KEY_DOWN, KEY_UP

from r_server.robot_server import Directions

class KeyboardController:
	'''Implements direct control using a connected USB keyboard'''
	def __init__(self, robot):
		self.robot = robot

		# Press PAGE UP then PAGE DOWN to type "foobar".
		#self.wHook = keyboard.add_hotkey('w', lambda: robot.move(Directions.Forward))
		#self.sHook = keyboard.add_hotkey('s', lambda: robot.move(Directions.Back))
		#self.aHook = keyboard.add_hotkey('a', lambda: robot.move(Directions.Left))
		#self.dHook = keyboard.add_hotkey('d', lambda: robot.move(Directions.Right))
		def handler(event):
			print('Got: ' + event)

		keyboard.listener.hotkeys[keyboard.os_keyboard.map_char(normalize_name('w'))] = handler
		keyboard.listener.add_handler(handler)
	def halt(self):
		#keyboard.remove_hotkey('w')
		#keyboard.remove_hotkey('s')
		#keyboard.remove_hotkey('a')
		#keyboard.remove_hotkey('s')
		#keyboard.remove_hotkey('d')
		pass



		


