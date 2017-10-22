'''
    Server implementation using sanic in python3 for speed
'''
from base64 import b64encode

from sanic import Sanic
from sanic.response import html

from jinja2 import Environment, PackageLoader

from .robot_server import RobotServer, Directions, Throttle
from .camera_server import CameraServer
from .keyboard_controller import KeyboardController

app = Sanic()  # pylint: disable=invalid-name

# Serves files from the static folder to the URL /static
app.static('/static', './r_server/static')

# Jinja2 templates
env = Environment(loader=PackageLoader('r_server', 'templates')) # pylint: disable=invalid-name

from ptvsd import enable_attach
enable_attach("kriekpi")

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
        message = await socket.recv()
        if message == 'hello':
            print('client connected')
            # send frame
            data = encode_frame()
            if data:
                await socket.send(data)
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
        if message == 'ack':
@app.route('/')
async def index(request):
    '''
        Main index handler
    '''
    from urllib.parse import urlparse
    parsed_url = urlparse(request.url)
    host = parsed_url.hostname + (':' + str(parsed_url.port) if parsed_url.port else '')

    template = env.get_template('main.html')
    html_content = template.render(host=host)
    return html(html_content)

if __name__ == "__main__":
    # Setup aux objects and store them on our app for namespace cleanness
    app.robot = RobotServer()
    app.camera = CameraServer()
    #app.keyboard_controller = KeyboardController(app.robot)

    app.run(host="0.0.0.0", port=8080)
