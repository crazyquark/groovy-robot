# Add Pixy 2 to path
from sys import path
path.insert(0, '../lib/pixy2/build/python_demos')

import pixy
from pixy import Uint32Array

from .camera import Camera

class PixyCamera(Camera):
    '''
        Class for using a Pixy2 camera board for robot vision
    '''

    def __init__(self):
        super(PixyCamera, self).__init__()

        pixy.init()
        pixy.change_prog('video')

    def get_frame(self):
        self.frame = Uint32Array(316*208)
        pixy.video_get_raw_frame(self.frame)

        self.compute_fps()

        return self.frame
