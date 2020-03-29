from time import time

class Camera:
    '''
        Base class for cameras
    '''

    def __init__(self):
        self.frame = None
        self.fps = 0
        
        self.prev_time = 0

    def dummy_frame(self):
        '''
            Filler frame
        '''
        with open('r_server/static/no-signal.jpg', 'rb') as image:
            return image.read()

    def compute_fps(self):
        current_time = time()
        if self.prev_time != 0:
            delta = current_time - self.prev_time
            self.fps = round(1/delta, 2)
        self.prev_time = current_time

    def get_frame(self):
        if self.frame is None:
            self.frame = self.dummy_frame()

        self.compute_fps()

        return self.frame