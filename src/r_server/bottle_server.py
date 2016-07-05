'''
	Server implementation using bottle
	See http://bottlepy.org/docs/dev/async.html
'''

from bottle import request, Bottle, abort, template
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
				robot.forward()
			elif (message == 's'):
				robot.backward()
			elif (message == 'a'):
				robot.left()
			elif (message == 'd'):
				robot.rightDir();

		except WebSocketError:
			break

@app.route('/')
def index():
	host = request.get_header('host')
	return template('r_server/main', host = host)


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def run():
	server = WSGIServer(("0.0.0.0", 8080), app,
						handler_class=WebSocketHandler)
	server.serve_forever()