'''
	Server implementation using bottle
	See http://bottlepy.org/docs/dev/async.html
'''

from bottle import request, Bottle, abort, template, static_file, Response
from robot_server import Directions, Throttle

app = Bottle()

@app.route('/ws')
def websocket():
	wsock = request.environ.get('wsgi.websocket')
	if not wsock:
		abort(400, 'Expected WebSocket request.')

	while True:
		try:
			message = wsock.receive()
			if (message == 'hello'):
				wsock.send('connected');
			elif (message == 'w'):
				robot.move(Directions.Forward)
			elif (message == 'W'):
				robot.stop(Directions.Forward)
			elif (message == 's'):
				robot.move(Directions.Back)
			elif (message == 'S'):
				robot.stop(Directions.Back)
			elif (message == 'a'):
				robot.move(Directions.Left)
			elif (message == 'A'):
				robot.stop(Directions.Left)
			elif (message == 'd'):
				robot.move(Directions.Right);
			elif (message == 'D'):
				robot.stop(Directions.Right)
			elif (message == 'x'):
				robot.speedAdjust(Throtle.Up)
			elif (message == 'z'):
				robot.speedAdjust(Throttle.Down)
			elif (message == ''):
				robot.stop()

		except WebSocketError:
			break

@app.route('/')
def index():
	host = request.get_header('host')
	return template('r_server/main.html', host = host, resolution = (800, 600))

@app.route('/images/<filename>')
def images(filename):
    return static_file(filename, root='../res/')

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def genStream(camera):
	'''Video streaming generator function.'''
	while True:
		try:
			frame = camera.getFrame()
		except:
			print 'Failed to get frame ' + str(frame)
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def stream():
	return Response(genStream(camera))

robot = None
def run(robotServer, cameraServer):
	global robot, camera
	robot = robotServer
	camera = cameraServer

	server = WSGIServer(("0.0.0.0", 8080), app,
						handler_class=WebSocketHandler)
	server.serve_forever()

def halt():
	robot.halt()