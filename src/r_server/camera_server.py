try:
    import picamera
    RUNNING_ON_PI = True
except:
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

        with picamera.PiCamera() as camera:
            # Camera setup
            camera.resolution = (800, 600)
            camera.hflip = True
            camera.vflip = True

            # Let camera warm up (??)
            camera.start_preview()
            time.sleep(2)

            # Create stream
            stream = io.BytesIO()

            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # Stop thread
                if not self.running:
                    return

                # Store frame
                stream.seek(0)
                self.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

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
