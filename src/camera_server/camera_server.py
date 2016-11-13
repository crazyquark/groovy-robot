try:
	import picamera
	runningOnPi = True
except:
	runningOnPi = False

from threading import Thread
import time, io

class CameraServer(Thread):
	'''
		An autostart camera thread that continously captures images from the camera for processing
		Inspired from https://github.com/crazyquark/flask-video-streaming/blob/master/camera_pi.py
	'''
	def __init__(self):
		Thread.__init__(self)

		self.resolution = (800, 600)
		self.running = True
		self.start()

	def run(self):
		if (not runningOnPi):
			if (not hasattr(self, 'frame')):
				with open('../res/wall-e-800.jpg', 'rb') as image:
					self.frame = image.read()
			return

		with picamera.PiCamera() as camera:
			# Camera setup
			camera.resolution = (800, 600)
			camera.hflip = True
			camera.vflip = True

			# Let camera warm up (??)
			camera.start_preview()
			time.sleep(2)
			
			# Create stream
			stream = io.BytesIO()
			
			for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
				# Stop thread
				if (not self.running):
					return

				# Store frame
				stream.seek(0)
				self.frame = stream.read()

				# reset stream for next frame
				stream.seek(0)
				stream.truncate()

	def getFrame(self):
		return self.frame

	def halt(self):
		self.running = False

