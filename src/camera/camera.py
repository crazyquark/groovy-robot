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
        with open('r_server/static/wall-e-800.jpg', 'rb') as image:
            return image.read()

    def get_frame(self):
        if not self.frame:
            self.frame = self.dummy_frame()
        
        current_time = time()
        if self.prev_time != 0:
            delta = current_time - self.prev_time
            self.fps = round(1/delta, 2)
        self.prev_time = current_time

        return self.frame