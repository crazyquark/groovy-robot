'''
    Server implementation using flask
    See http://bottlepy.org/docs/dev/async.html
'''

from flask import Flask, render_template as template, request, make_response, jsonify, Response
from flask_sockets import Sockets
from robot_server import Directions, Throttle

app = Flask(__name__, template_folder='.', static_folder='../../res/') # pylint: disable=invalid-name
app.debug = True
sockets = Sockets(app) # pylint: disable=invalid-name

@sockets.route('/ws')
def websocket(wsock):
    '''
        Server websocket
    '''
    while not wsock.closed:
        try:
            message = wsock.receive()
            if message == 'hello':
                print 'connected'
            elif message == 'w':
                app.robot.move(Directions.Forward)
            elif message == 'W':
                app.robot.stop(Directions.Forward)
            elif message == 's':
                app.robot.move(Directions.Back)
            elif message == 'S':
                app.robot.stop(Directions.Back)
            elif message == 'a':
                app.robot.move(Directions.Left)
            elif message == 'A':
                app.robot.stop(Directions.Left)
            elif message == 'd':
                app.robot.move(Directions.Right)
            elif message == 'D':
                app.robot.stop(Directions.Right)
            elif message == 'x':
                app.robot.speed_adjust(Throttle.Up)
            elif message == 'z':
                app.robot.speed_adjust(Throttle.Down)
            elif message == '':
                app.robot.stop()
        except WebSocketError as err:
            print repr(err)
            break

@app.route('/')
def index():
    from urlparse import urlparse
    parsedUrl = urlparse(request.url)
    host = parsedUrl.hostname + (':' + str(parsedUrl.port) if parsedUrl.port else '')
    
    return template('main.html', host = host, resolution = (800, 600))

@app.route('/images/<filename>')
def images(filename):
    return app.send_static_file(filename)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

app.robot = None
app.camera = None
def run(robotServer, cameraServer):
    app.robot = robotServer
    app.camera = cameraServer

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    server = pywsgi.WSGIServer(('', 8080), app, handler_class=WebSocketHandler)
    server.serve_forever()

def halt():
    app.robot.halt()
