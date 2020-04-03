import queue
import pyaudio
from ctypes import *

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
MAX_FRAMES = 20

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        # self.queue = queue.Queue(maxsize=MAX_FRAMES)

        self.alsaMessageSuppress()
        self.audio = pyaudio.PyAudio()
        
        self.stream = self.audio.open(format=FORMAT,
            rate=RATE, input=True, 
            channels=CHANNELS,
            frames_per_buffer=CHUNK)

    def get_frame(self):
        frame = self.stream.read(CHUNK)
        return frame

    def close(self):
        ''' Close stream '''
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def alsaMessageSuppress(self):
        ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
        def py_error_handler(filename, line, function, err, fmt):
            print(err)
        
        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
        asound = cdll.LoadLibrary('libasound.so.2')
        # Set error handler
        asound.snd_lib_error_set_handler(c_error_handler)
