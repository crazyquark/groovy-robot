from io import BytesIO

import queue
import pyaudio

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 4096
MAX_FRAMES = 5

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.queue = queue.Queue()

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT,
            rate=RATE, input=True, 
            channels=CHANNELS,
            frames_per_buffer=CHUNK,
            stream_callback=self.stream_callback)
        self.stream.start_stream()

    def stream_callback(self, in_data, frame_count, time_info, status_flags):
        ''' Get an audio chunk from internal stream '''
        data = in_data.copy()
        self.queue.put(data)
        return (data, pyaudio.paContinue)

    def close(self):
        ''' Close stream '''
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
