'''
    Server implementation using sanic in python3 for speed
'''
from base64 import b64encode
from asyncio import sleep

from sanic import Sanic
from sanic.response import html
from sanic.exceptions import RequestTimeout
from websockets.exceptions import ConnectionClosed

from jinja2 import Environment, PackageLoader

from .robot_server import RobotServer, Directions, CameraMovement, Throttle
from .camera_server import CameraServer
# from .keyboard_controller import KeyboardController
from .ps3_controller import PS3Controller
from .display import PiDisplay
from .audio_process import AudioProcess
from .mic_capture import MicCapture

app = Sanic()  # pylint: disable=invalid-name

# Serves files from the static folder to the URL /static
app.static('/static', './r_server/static')

# Jinja2 templates
env = Environment(loader=PackageLoader('r_server', 'templates')
                  )  # pylint: disable=invalid-name

from ptvsd import enable_attach, wait_for_attach
enable_attach(redirect_output=True)
# wait_for_attach()

@app.websocket('/ws')
async def websocket(_, socket):
    '''
        Keyboard websocket
    '''
    def encode_frame():
        '''
            Base64 image
        '''
        if app.camera:
            frame = app.camera.get_frame()
            data = b64encode(frame)

        return data.decode('utf-8')

    while True:
        try:
            message = await socket.recv()
        except (ConnectionClosed, RequestTimeout):
            break

        if message == '1':
            # send frame
            data = encode_frame()
            if data:
                try:
                    await socket.send(data)
                except (ConnectionClosed, RequestTimeout):
                    break

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
        elif message == 'q':
            app.robot.tilt_camera(CameraMovement.Up)
        elif message == 'e':
            app.robot.tilt_camera(CameraMovement.Down)
        elif message == 'Q' or message == 'E':
            app.robot.tilt_camera(CameraMovement.Idle)


@app.websocket('/mic')
async def mic_websocket(_, socket):
    while True:
        try:
            await socket.recv()
        except (ConnectionClosed, RequestTimeout):
            break

        audio_chunk = app.mic_queue.get()
        wave = MicCapture.encode_data(audio_chunk)

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

    app.robot.halt()
    app.camera.halt()
    app.ps3controller.halt()
    app.display.halt()

    return app.stop()

if __name__ == "__main__":
    # Setup aux objects and store them on our app for namespace cleanness
    app.robot = RobotServer()
    app.camera = CameraServer()
    #app.keyboard_controller = KeyboardController(app.robot)
    app.ps3controller = PS3Controller(app.robot)
    app.display = PiDisplay()

    app.mic_queue = AudioProcess.start_capture()

    app.run(host="0.0.0.0", port=8080, workers=1)
