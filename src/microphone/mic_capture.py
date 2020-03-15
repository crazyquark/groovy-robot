import queue
import time
from io import BytesIO

import numpy
import sounddevice as sd
import soundfile as sf

SAMPLEWIDTH = 2 # int16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
MAX_FRAMES = 5

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.stream = sd.InputStream(samplerate=RATE, 
            channels=CHANNELS, device=1, 
            blocksize=CHUNK,
            callback=self.stream_callback)

        self.queue = queue.Queue()

        self.stream.start()

    def stream_callback(self, in_data, frame_count, time_info, status):
        ''' Get an audio chunk from internal stream '''
        self.queue.put(in_data.copy())

    @staticmethod
    def encode_data(raw_data):
        # convert current chunk    
        memory_file = BytesIO()
        wave_file = sf.SoundFile(memory_file, mode='x', samplerate=RATE, format='wav',
            channels=CHANNELS)
        wave_file.write(raw_data)
        wave_file.close()

        memory_file.seek(0)
        data = memory_file.read()
        memory_file.close()

        return data


    def close(self):
        ''' Close stream '''
        self.stream.close()
