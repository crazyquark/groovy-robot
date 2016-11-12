from threading import Thread
import shlex, subprocess, os

class Camera(Thread):
	"""A camera thread that launches mjpeg-streamer for remote viewing"""
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		streamerPath = os.path.join(os.getcwd(), '../lib/mjpg-streamer/mjpg-streamer-experimental')
		exePath = os.path.join(streamerPath, 'mjpg_streamer')

		if os.path.isfile(exePath):
			wwwPath = os.path.join(streamerPath, 'www')

			cmd = shlex.split(exePath + ' -o "output_http.so -w ' + wwwPath + ' -p 9090" -i "input_raspicam.so"')

			runEnv = os.environ.copy()
			runEnv['LD_LIBRARY_PATH'] = streamerPath

			self.streamer = subprocess.Popen(cmd, env = runEnv)
		
		else:
			print 'Looks like we are missing mjpg-streamer'

	def halt(self):
		if (hasattr(self, 'streamer')):
			self.streamer.kill()

