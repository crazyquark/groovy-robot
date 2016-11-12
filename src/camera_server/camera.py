from threading import Thread
import shlex, subprocess, os

class Camera(Thread):
	"""A camera thread that launches mjpeg-streamer for remote viewing"""
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		streamerPath = os.path.join(os.getcwd(), '../lib/mjpeg-streamer/mjpeg-streamer-experimental')
		exePath = os.path.join(streamerPath, 'mjpg_streamer')

		if os.path.isfile(exePath):

			cmd = shlex.split(exePath + ' -o "output_http.so -w ./www -p 9090" -i "input_raspicam.so"')

			runEnv = os.environ.copy()
			runEnv['LD_LIBRARY_PATH'] = streamerPath

			subprocess.Popen(cmd, env = runEnv)
		
		else:
			print 'Looks like we are missing mjpg-streamer'

