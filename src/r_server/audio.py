import pyaudio
import wave
import time
from io import BytesIO
from threading import Thread

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 4096
RECORD_SECONDS = 5


class MicCapture(Thread):
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      input_device_index=2,
                                      frames_per_buffer=CHUNK)
        self.create_buffer()
        self.is_running = True
        self.start()

    def create_buffer(self):
        self.memory_file = BytesIO()
        self.buffer = wave.open(self.memory_file, 'wb')
        self.buffer.setnchannels(CHANNELS)
        self.buffer.setsampwidth(self.audio.get_sample_size(FORMAT))
        self.buffer.setframerate(RATE)

    def run(self):
        while self.is_running:
            self.get_audio_chunk()

    def get_data(self):
        self.memory_file.seek(0)
        data = self.memory_file.read()
        
        self.memory_file.close()
        self.buffer.close()

        self.create_buffer()

        return data

    def get_audio_chunk(self):
        ''' Get an audio chunk from internal stream '''
        raw_data = self.stream.read(CHUNK)
        self.buffer.writeframes(raw_data)

    def close(self):
        ''' Close stream '''
        self.is_running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
