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
                wsock.send('ack')
            elif message == 'W':
                app.robot.stop(Directions.Forward)
                wsock.send('ack')
            elif message == 's':
                app.robot.move(Directions.Back)
                wsock.send('ack')
            elif message == 'S':
                app.robot.stop(Directions.Back)
                wsock.send('ack')
            elif message == 'a':
                app.robot.move(Directions.Left)
                wsock.send('ack')
            elif message == 'A':
                app.robot.stop(Directions.Left)
                wsock.send('ack')
            elif message == 'd':
                app.robot.move(Directions.Right)
                wsock.send('ack')
            elif message == 'D':
                app.robot.stop(Directions.Right)
                wsock.send('ack')
            elif message == 'x':
                app.robot.speed_adjust(Throttle.Up)
                wsock.send('ack')
            elif message == 'z':
                app.robot.speed_adjust(Throttle.Down)
                wsock.send('ack')
            elif message == '':
                app.robot.stop()
                wsock.send('ack')
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

def genStream(camera):
    '''Video streaming generator function.'''
    while True:
        frame = app.camera.getFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stream')
def stream():
    global camera
    return Response(genStream(camera), mimetype='multipart/x-mixed-replace; boundary=frame') 

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
