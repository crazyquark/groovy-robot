'''
	Server implementation using bottle
	See http://bottlepy.org/docs/dev/async.html
'''

from bottle import request, Bottle, abort, template, static_file
from r_server.robot_server import RobotServer

app = Bottle()
robot = RobotServer()

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
				robot.move(1)
			elif (message == 's'):
				robot.move(-1)
			elif (message == 'a'):
				robot.move(2)
			elif (message == 'd'):
				robot.move(3);
			elif (message == 'x'):
				robot.speedAdjust(1)
			elif (message == 'z'):
				robot.speedAdjust(-1);
			elif (message == 'st'):
				robot.stop()

		except WebSocketError:
			break

@app.route('/')
def index():
	host = request.get_header('host')
	return template('r_server/main.html', host = host)

@app.route('/images/<filename>')
def images(filename):
    return static_file(filename, root='../res/')

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def run():
	server = WSGIServer(("0.0.0.0", 8080), app,
						handler_class=WebSocketHandler)
	server.serve_forever()