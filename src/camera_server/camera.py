from threading import Thread
import shlex, subprocess, os

class Camera(Thread):
	"""A camera thread that launches mjpeg-streamer for remote viewing"""
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		if os.path.isfile(self.streamerPath):
			streamerPath = './lib/mjpeg-streamer/mjpeg-streamer-experimental'

			cmd = shlex.split(streamerPath + '/mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"')

			runEnv = os.environ.copy()
			runEnv['LD_LIBRARY_PATH'] = streamerPath

			subprocess.Popen(cmd, env = runEnv)
		
		else:
			print 'Looks like we are missing mjpg-streamer'

