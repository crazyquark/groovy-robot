# Add Pixy 2 to path
from sys import path
path.insert(0, '../lib/pixy2/build/python_demos')

import pixy
from ctypes import *
from pixy import *

from .camera import Camera


class Blocks (Structure):
    _fields_ = [("m_signature", c_uint),
                ("m_x", c_uint),
                ("m_y", c_uint),
                ("m_width", c_uint),
                ("m_height", c_uint),
                ("m_angle", c_uint),
                ("m_index", c_uint),
                ("m_age", c_uint)]


class PixyCamera(Camera):
    '''
        Class for using a Pixy2 camera board for robot vision
    '''

    def __init__(self):
        super(PixyCamera, self).__init__()

        pixy.init()
        pixy.change_prog('video')

    def get_frame(self):
        self.frame = video_get_RGB(158, 104)

        self.compute_fps()

        return self.frame
