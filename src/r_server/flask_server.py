'''
	Server implementation using bottle
	See http://bottlepy.org/docs/dev/async.html
'''

from flask import Flask, render_template as template, request, make_response, jsonify, Response
from flask_sockets import Sockets
from robot_server import Directions, Throttle

app = Flask(__name__, template_folder = '.', static_folder = '../../res/')
app.debug = True
sockets = Sockets(app)

@sockets.route('/ws')
def websocket(wsock):
	while not wsock.closed:
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
				robot.move(Directions.Left)
			elif (message == 'A'):
				robot.stop(Directions.Left)
			elif (message == 'd'):
				robot.move(Directions.Right);
			elif (message == 'D'):
				robot.stop(Directions.Right)
			elif (message == 'x'):
				robot.speedAdjust(Throttle.Up)
			elif (message == 'z'):
				robot.speedAdjust(Throttle.Down)
			elif (message == ''):
				robot.stop()
		except WebSocketError as err:
			print repr(err)
			break

@app.route('/')
def index():
	return template('main.html', host = 'localhost:8080', resolution = (800, 600))

@app.route('/images/<filename>')
def images(filename):
    return app.send_static_file(filename)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def genStream(camera):
	'''Video streaming generator function.'''
	frame = None
	while True:
		frame = camera.getFrame()
		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def stream():
	global camera
	return Response(genStream(camera), mimetype='multipart/x-mixed-replace; boundary=frame') 

robot = None
def run(robotServer, cameraServer):
	global robot, camera
	robot = robotServer
	camera = cameraServer

	from gevent import pywsgi
	from geventwebsocket.handler import WebSocketHandler
	server = pywsgi.WSGIServer(('', 8080), app, handler_class=WebSocketHandler)
	server.serve_forever()

def halt():
	robot.halt()