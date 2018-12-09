'''
    Server implementation using sanic in python3 for speed
'''
from asyncio import sleep

from sanic import Sanic
from sanic.response import html
from sanic.exceptions import RequestTimeout
from websockets.exceptions import ConnectionClosed

from jinja2 import Environment, PackageLoader

from .robot_server import RobotServer, Directions, CameraMovement, Throttle
from microphone.mic_capture import MicCapture

from microphone.audio_process import AudioProcess
from camera.camera_process import CameraProcess
from camera.pixy_camera import PixyCamera

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
    while True:
        try:
            message = await socket.recv()
        except (ConnectionClosed, RequestTimeout):
            break

        if message == '1':
            # send frame
            frame = app.camera_queue.get()
            data = CameraProcess.encode_frame(frame)
            if data:
                try:
                    await socket.send(data)
                except (ConnectionClosed, RequestTimeout):
                    break

        elif message == 'w':
            app.robot_queue.put_nowait(Directions.Forward)
        elif message == 'W':
            app.robot_queue.put_nowait(Directions.Forward)
        elif message == 's':
            app.robot_queue.put_nowait(Directions.Back)
        elif message == 'S':
            app.robot_queue.put_nowait(Directions.Back)
        elif message == 'a':
            app.robot_queue.put_nowait(Directions.Left)
        elif message == 'A':
            app.robot_queue.put_nowait(Directions.Left)
        elif message == 'd':
            app.robot_queue.put_nowait(Directions.Right)
        elif message == 'D':
            app.robot_queue.put_nowait(Directions.Right)
        elif message == 'x':
            app.robot_queue.put_nowait(Throttle.Up)
        elif message == 'z':
            app.robot_queue.put_nowait(Throttle.Down)
        elif message == 'q':
            app.robot_queue.put_nowait(CameraMovement.Up)
        elif message == 'e':
            app.robot_queue.put_nowait(CameraMovement.Down)
        elif message == 'Q' or message == 'E':
            app.robot_queue.put_nowait(CameraMovement.Idle)


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
    CameraProcess.stop_camera()
    RobotServer.stop_robot()

    app.camera.halt()
    app.display.halt()

    return app.stop()

if __name__ == "__main__":
    # Setup aux objects and store them on our app for namespace cleanness

    app.mic_queue = AudioProcess.start_capture()
    app.camera_queue = CameraProcess.start_camera(camera_type=PixyCamera)
    app.robot_queue = RobotServer.start_robot()

    app.run(host='0.0.0.0', port=8080, workers=1)
