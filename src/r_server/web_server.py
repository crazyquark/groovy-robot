'''
    Server implementation using sanic in python3 for speed
'''
from asyncio import sleep

from sanic import Sanic
from sanic.response import json
from sanic.response import html
from sanic.exceptions import RequestTimeout
from websockets.exceptions import ConnectionClosed

from jinja2 import Environment, PackageLoader

from r_server.robot_process import RobotProcess, Directions, CameraMovement, Throttle
from microphone.mic_capture import MicCapture

from microphone.audio_process import AudioProcess
from camera.camera_process import CameraProcess
from camera.pixy_camera import PixyCamera
from camera.camera import Camera

app = Sanic()  # pylint: disable=invalid-name

# Serves files from the static folder to the URL /static
app.static('/static', './r_server/static')
app.static('/favicon.ico', './r_server/static/favicon.ico')

# Jinja2 templates
env = Environment(loader=PackageLoader('r_server', 'templates')
                  )  # pylint: disable=invalid-name

# from ptvsd import enable_attach, wait_for_attach
# enable_attach(redirect_output=True)
# wait_for_attach()


@app.websocket('/ws')
async def websocket(_, socket):
    '''
        Main command websocket
    '''
    while app.is_running:
        try:
            message = await socket.recv()
        except (ConnectionClosed, RequestTimeout):
            break

        if message == '1':
            # send frame
            try:
                frame = app.camera_queue.get_nowait()
                data = CameraProcess.encode_frame(frame)
            except:
                continue
            if data:
                try:
                    await socket.send(data)
                except (ConnectionClosed, RequestTimeout):
                    break

        elif message == 'w':
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

@app.websocket('/mic')
async def mic_websocket(_, socket):
    while app.is_running:
        try:
            await socket.recv()
        except (ConnectionClosed, RequestTimeout):
            break

        audio_chunk = app.mic_queue.get()
        wave = bytes(audio_chunk)

        try:
            await socket.send(wave)
        except (ConnectionClosed, RequestTimeout):
            break


@app.route('/')
async def index(request):
    '''
        Main index handler
    '''
    from urllib.parse import urlparse
    parsed_url = urlparse(request.url)
    host = parsed_url.hostname + \
        (':' + str(parsed_url.port) if parsed_url.port else '')

    template = env.get_template('main.html')
    html_content = template.render(host=host)
    return html(html_content)


@app.route('/halt')
async def halt(_):
    '''
        Stop web server
    '''
    AudioProcess.stop_capture()
    CameraProcess.stop_camera()
    RobotProcess.stop_robot()

    app.stop()

    return json({'message':'OK'})



def start_web_server(running_on_arm):
    # Setup aux objects and store them on our app for namespace cleanness
    app.mic_queue = AudioProcess.start_capture()
    app.camera_queue = CameraProcess.start_camera(camera_type=PixyCamera if running_on_arm else Camera)
    app.robot_queue = RobotProcess.start_robot(running_on_arm)

    app.run(host='0.0.0.0', port=8080, workers=1)
