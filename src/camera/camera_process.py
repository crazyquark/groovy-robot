from multiprocessing import Queue
import cv2

from debug.debuggable_process import DebuggableProcess
from .camera import Camera

# Frame buffer size
MAX_FRAMES = 5


class CameraProcess(DebuggableProcess):
    '''
        Class for a forked camera process
    '''

    def __init__(self, queue, camera_type=Camera):
        '''
            Creates a new camera process uing the given camera_type
        '''
        super(CameraProcess, self).__init__()
        self.queue = queue
        self.camera_type = camera_type

    def run(self):
        self.enable_debug(1212)
        self.enable_logging('camera')

        camera = self.camera_type()

        while True:
            frame = camera.get_frame()

            if frame:
                try:
                    self.queue.put_nowait(frame)
                except:
                    # full exception happens because empty and full are unreliable
                    continue

    @classmethod
    def start_camera(cls, camera_type=Camera):
        if hasattr(cls, 'instance'):
            return cls.queue

        cls.queue = Queue(MAX_FRAMES)
        cls.instance = CameraProcess(cls.queue, camera_type)
        cls.instance.start()

        return cls.queue

    @classmethod
    def stop_camera(cls):
        if hasattr(cls, 'instance'):
            cls.instance.terminate()

    @staticmethod
    def encode_frame(frame):
        '''
            Base64 image
        '''
        if frame:
            (flag, frame) = cv2.imencode(".jpg", frame)

        return frame if flag else None
