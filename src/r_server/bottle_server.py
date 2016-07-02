'''
	Server implementation using bottle
	See http://bottlepy.org/docs/dev/async.html
'''

from bottle import request, Bottle, abort, template
from r_server.robot_server import RobotServer

app = Bottle()

@app.route('/ws')
def websocket():
	wsock = request.environ.get('wsgi.websocket')
	if not wsock:
		abort(400, 'Expected WebSocket request.')

	while True:
		try:
			message = wsock.receive()
			wsock.send("Your message was: %r" % message)
		except WebSocketError:
			break

@app.route('/')
def index():
	return template('r_server/main')


from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

def run():
	server = WSGIServer(("0.0.0.0", 8080), app,
						handler_class=WebSocketHandler)
	server.serve_forever()