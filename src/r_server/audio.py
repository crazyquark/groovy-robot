import pyaudio
import wave
import time
from io import BytesIO
from collections import deque
from threading import Thread

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
MAX_FRAMES = 5

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK, stream_callback=self.stream_callback)

        self.frames = deque([], MAX_FRAMES)
        self.stream.start_stream()

    def stream_callback(self, in_data, frame_count, time_info, status):
        ''' Get an audio chunk from internal stream '''
        self.frames.append(in_data)

        return (in_data, pyaudio.paContinue)

    def get_data(self):
        if len(self.frames) == 0:
            return
        
        # convert current chunk    
        memory_file = BytesIO()
        wave_file = wave.open(memory_file, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(self.frames.pop())
        wave_file.close()

        memory_file.seek(0)
        data = memory_file.read()
        memory_file.close()
        
        return data


    def close(self):
        ''' Close stream '''
        self.is_running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
