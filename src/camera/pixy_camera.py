# Add Pixy 2 to path
from sys import path
path.insert(0, '../lib/pixy2/build/python_demos')

import pixy
from PIL import Image

from .camera import Camera


class PixyCamera(Camera):
    '''
        Class for using a Pixy2 camera board for robot vision
    '''

    def __init__(self):
        super(PixyCamera, self).__init__()

        pixy.init()
        pixy.change_prog('video')

        self.frame_width = 316
        self.frame_height = 208

    def get_frame(self):
        raw_frame = pixy.video_get_raw_frame(
            self.frame_width*self.frame_height*3)
        self.frame = Image.fromarray(raw_frame.reshape(
            self.frame_height, self.frame_width, 3))

        self.compute_fps()

        return self.frame
