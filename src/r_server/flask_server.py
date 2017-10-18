'''
    Server implementation using flask
    See http://bottlepy.org/docs/dev/async.html
'''

from flask import Flask, Blueprint, render_template as template, request, make_response, jsonify, Response
from flask_sockets import Sockets
from robot_server import Directions, Throttle

html = Blueprint('html', __name__, template_folder = '.', static_folder = '../../res/')
ws = Blueprint('ws', __name__)

@ws.route('/ws')
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
                robot.move(Directions.Forward)
                wsock.send('ack')
            elif message == 'W':
                robot.stop(Directions.Forward)
                wsock.send('ack')
            elif message == 's':
                robot.move(Directions.Back)
                wsock.send('ack')
            elif message == 'S':
                robot.stop(Directions.Back)
                wsock.send('ack')
            elif message == 'a':
                robot.move(Directions.Left)
                wsock.send('ack')
            elif message == 'A':
                robot.stop(Directions.Left)
                wsock.send('ack')
            elif message == 'd':
                robot.move(Directions.Right)
                wsock.send('ack')
            elif message == 'D':
                robot.stop(Directions.Right)
                wsock.send('ack')
            elif message == 'x':
                robot.speed_adjust(Throttle.Up)
                wsock.send('ack')
            elif message == 'z':
                robot.speed_adjust(Throttle.Down)
                wsock.send('ack')
            elif message == '':
                robot.stop()
                wsock.send('ack')
        except WebSocketError as err:
            print repr(err)
            break

@html.route('/')
def index():
    from urlparse import urlparse
    parsedUrl = urlparse(request.url)
    host = parsedUrl.hostname + (':' + str(parsedUrl.port) if parsedUrl.port else '')
    
    return template('main.html', host = host, resolution = (800, 600))

@html.route('/images/<filename>')
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

@html.route('/stream')
def stream():
    global camera
    return Response(genStream(camera), mimetype='multipart/x-mixed-replace; boundary=frame') 

app = Flask(__name__)
sockets = Sockets(app)

app.register_blueprint(html, url_prefix='/')
app.register_blueprint(ws, url_prefix='/')

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