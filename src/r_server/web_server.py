'''
    Server implementation using flask
    See http://bottlepy.org/docs/dev/async.html
'''
from threading import Thread

from flask import Flask, render_template as template, request, make_response, jsonify, Response
from flask_sockets import Sockets

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

from base64 import b64encode

from robot_server import Directions, Throttle
from robot_server import RobotServer
from camera_server import CameraServer
from keyboard_controller import KeyboardController

app = Flask(__name__, template_folder='templates', static_folder='static') # pylint: disable=invalid-name
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
                print 'client connected'
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

@sockets.route('/camera')
def websocket_camera(wsock):
    '''
        Camera websocket
    '''

    def run_camera():
        '''
            Thread based websocket camera sender
        '''
        def encode_frame():
            '''
                Base64 image
            '''
            if app.camera:
                frame = app.camera.get_frame()
                data = b64encode(frame)

                return data
        while not wsock.closed:
            try:
                data = encode_frame()
                if data:
                    wsock.send(data)
            except WebSocketError as err:
                print repr(err)
                break
    camera_thread = Thread(target=run_camera)
    camera_thread.start()

@app.route('/')
def index():
    '''
        Main index handler
    '''
    from urlparse import urlparse
    parsed_url = urlparse(request.url)
    host = parsed_url.hostname + (':' + str(parsed_url.port) if parsed_url.port else '')

    return template('main.html', host=host)

@app.route('/images/<filename>')
def images(filename):
    '''
        Server images
    '''
    return app.send_static_file(filename)

# setup aux objects
if __name__ == '__main__':
    app.robot = RobotServer()
    app.camera = CameraServer()
    app.keyboard_controller = KeyboardController(app.robot)

    try:
        server = WSGIServer(('', 8080), app, handler_class=WebSocketHandler)  # pylint: disable=invalid-name
        server.serve_forever()
    except KeyboardInterrupt:
        server.stop()
        app.robot.halt()
        app.camera.halt()
        app.keyboard_controller.halt()
