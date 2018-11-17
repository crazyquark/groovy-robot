from multiprocessing import Process, Queue

from .camera import Camera

# Frame buffer size
MAX_FRAMES = 5

class CameraProcess(Process):
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
        camera = self.camera_type()

        while True:
            frame = camera.get_frame()

            if frame:
                # Make room in the queue
                if self.queue.full():
                    while not self.queue.empty():
                        try:
                            self.queue.get_nowait()
                        except:
                            # empty queue error
                            break
                try:
                    self.queue.put_nowait(frame)
                except:
                    # full exception happens because empty and full are unreliable
                    continue

    @classmethod
    def start_camera(cls):
        if hasattr(cls, 'instance'):
            return cls.queue

        cls.queue = Queue(MAX_FRAMES)
        cls.instance = CameraProcess(cls.queue)
        cls.instance.start()

        return cls.queue
    
    @staticmethod
    def stop_camera(cls):
        if hasattr(cls, 'instance'):
            cls.instance.terminate()
