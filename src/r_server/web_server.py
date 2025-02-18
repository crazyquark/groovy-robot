'''
    Web server implementation
'''
# See https://github.com/eventlet/eventlet/issues/592
import eventlet
eventlet.monkey_patch()
import __original_module_threading as orig_threading
import threading
orig_threading.current_thread.__globals__['_active'] = threading._active

from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO, emit
from multiprocessing import Queue

from r_server.robot_process import RobotProcess, Directions, CameraMovement, Throttle

from microphone.audio_process import AudioProcess
from camera.camera_process import CameraProcess
from camera.pi_camera import PiCamera
from camera.camera import Camera

# Detect platform
from platform import uname
running_on_arm = uname().machine != 'x86_64'

# Configure template and static paths
app = Flask(__name__)
app.config['SECRET_KEY'] = 'STZjV3G7'
socketio = SocketIO(app, message_queue='redis://')

# @app.websocket('/mic')
# async def mic_websocket(_, socket):
#     while app.is_running:
#         try:
#             await socket.recv()
#         except (ConnectionClosed, RequestTimeout):
#             break

#         audio_chunk = app.mic_queue.get()
#         wave = bytes(audio_chunk)

#         try:
#             await socket.send(wave)
#         except (ConnectionClosed, RequestTimeout):
#             break


@socketio.on('connect', namespace='/control')
def control_connect():
    emit('status', 'connected')


@socketio.on('connect', namespace='/audio')
def audio_connect():
    emit('status', 'connected')

@socketio.on('control_key', namespace='/control')
def on_control_key(message):
    if message == 'w':
        send_robot_message(Directions.Forward)
    elif message == 'W':
        send_robot_message(Directions.Forward)
    elif message == 's':
        send_robot_message(Directions.Back)
    elif message == 'S':
        send_robot_message(Directions.Back)
    elif message == 'a':
        send_robot_message(Directions.Left)
    elif message == 'A':
        send_robot_message(Directions.Left)
    elif message == 'd':
        send_robot_message(Directions.Right)
    elif message == 'D':
        send_robot_message(Directions.Right)
    elif message == 'x':
        send_robot_message(Throttle.Up)
    elif message == 'z':
        send_robot_message(Throttle.Down)
    elif message == 'q':
        send_robot_message(CameraMovement.Up)
    elif message == 'e':
        send_robot_message(CameraMovement.Down)
    elif message == 'Q' or message == 'E':
        send_robot_message(CameraMovement.Idle)

def send_robot_message(message):
    try:
        app.robot_queue.put_nowait(message)
    except:
        pass

@app.route('/')
def index():
    '''
        Main index handler
    '''
    return render_template('main.html')

def gen_frame():
    while True:
        if not app.camera_queue.empty():
            frame = app.camera_queue.get_nowait()
            encoded_image = CameraProcess.encode_frame(frame)
            if not encoded_image is None:
                yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
                        bytearray(encoded_image) + b'\r\n')


@app.route('/video')
def video():
    '''
        Video stream
    '''
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/halt')
def halt():
    '''
        Stop web server
    '''
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    shutdown()

    print('Shutting down...')

    return 'OK'


if __name__ == '__main__':
    # Start secondary processes
    app.camera_queue = CameraProcess.start_camera(camera_type=PiCamera if running_on_arm else Camera)
    app.robot_queue = RobotProcess.start_robot(running_on_arm)
    AudioProcess.start_capture()

    socketio.run(app, host='0.0.0.0', port=8080, debug=False)
