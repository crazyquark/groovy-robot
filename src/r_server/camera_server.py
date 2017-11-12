try:
    import picamera
    RUNNING_ON_PI = True
except ImportError:
    RUNNING_ON_PI = False

from threading import Thread
import time, io
import cv2
import numpy as np

class CameraServer(Thread):
    '''
        An autostart camera thread that continously captures images from the camera for processing
        Inspired from https://github.com/crazyquark/flask-video-streaming/blob/master/camera_pi.py
    '''
    def __init__(self):
        Thread.__init__(self)

        self.resolution = (800, 600)
        self.running = True

        self.camera = None

        if RUNNING_ON_PI:
            # Create stream
            self.stream = io.BytesIO()

            # Camera setup
            self.camera = picamera.PiCamera()

            # Let camera warm up (??)
            self.camera.start_preview()
            time.sleep(2)

            self.camera.resolution = (800, 600)
            self.camera.framerate = 25
            self.camera.hflip = True
            self.camera.vflip = True

        self.frame = None
        self.dummy_frame()

        self.start()

    def dummy_frame(self):
        '''
            If not on RPi return a dummy frame
        '''
        if not hasattr(self, 'frame'):
            with open('./r_server/static/wall-e-800.jpg', 'rb') as image:
                self.frame = image.read()

    def run(self):
        if not RUNNING_ON_PI:
            return

        for _ in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port=True):
            # Stop thread
            if not self.running:
                return

            # Store frame
            self.stream.seek(0)
            self.frame = self.stream.read()

            # reset stream for next frame
            self.stream.seek(0)
            self.stream.truncate()

    def to_grayscale(self, frame):
        '''
            IMG to grayscale as numpy array
        '''
        data = np.fromstring(frame, dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        result = cv2.imencode('.jpg', gray)
        data = np.array(result[1], dtype=np.uint8).tostring()

        return data

    def get_frame(self):
        '''
            Get current camera frame
        '''
        return self.to_grayscale(self.frame)

    def halt(self):
        '''
            Stop server thread
        '''
        self.running = False
        if self.camera:
            self.camera.close()
            self.stream.close()
