from threading import Thread
import shlex, subprocess, os

class CameraServer(Thread):
	"""A camera thread that launches mjpeg-streamer for remote viewing"""
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		pass

	def halt(self):
		pass

