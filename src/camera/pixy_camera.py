# Add Pixy 2 to path
from sys import path
path.insert(0, '../lib/pixy2/build/python_demos')

from .camera import Camera

class PixyCamera(Camera):
    '''
        Class for using a Pixy2 camera board for robot vision
    '''
    def __init__(self):
        super(PixyCamera, self).__init__()
    
