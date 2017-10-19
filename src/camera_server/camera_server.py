try:
	import picamera
	runningOnPi = True
except:
	runningOnPi = False

from threading import Thread
import time, io
import cv2
import numpy as np

class CameraServer(Thread):
	'''
		An autostart camera thread that continously captures images from the camera for processing
		Inspired from https://github.com/crazyquark/flask-video-streaming/blob/master/camera_pi.py
	'''
	def __init__(self):
		Thread.__init__(self)

		self.resolution = (800, 600)
		self.running = True
		self.dummyFrame() 
		self.start()
	
	def dummyFrame(self):
		if (not hasattr(self, 'frame')):
			with open('./r_server/static/wall-e-800.jpg', 'rb') as image:
				self.frame = image.read()

	def run(self):
		if (not runningOnPi):
			self.dummyFrame()
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
	
	def toGrayscale(self, frame):
		data = np.fromstring(frame, dtype=np.uint8)
		image = cv2.imdecode(data, cv2.IMREAD_COLOR)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		
		retImage = cv2.imencode('.jpg', gray)
		retData = np.array(retImage[1], dtype=np.uint8).tostring()
	
		return retData

	def getFrame(self):
		return self.toGrayscale(self.frame)

	def halt(self):
		self.running = False

