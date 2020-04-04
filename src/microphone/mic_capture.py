import queue
import time

import sounddevice as sd

SAMPLEWIDTH = 2 # int16
CHANNELS = 1
RATE = 44100
CHUNK = 4096
MAX_FRAMES = 5

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.stream = sd.InputStream(samplerate=RATE, 
            channels=CHANNELS, device=0, 
            blocksize=CHUNK,
            callback=self.stream_callback)

        self.queue = queue.Queue()

        self.stream.start()

    def stream_callback(self, in_data, frame_count, time_info, status):
        ''' Get an audio chunk from internal stream '''
        self.queue.put(in_data.copy())

    def close(self):
        ''' Close stream '''
        self.stream.close()
