import pyaudio
import wave
import time
from io import BytesIO
from threading import Thread

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 4*4096
RECORD_SECONDS = 5

class MicCapture(Thread):
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      input_device_index=2,
                                      frames_per_buffer=CHUNK)

        Thread.__init__(self)

        self.frames = []
        self.is_running = True
        self.clients = 0

        self.start()
    
    def run(self):
        while self.is_running:
            # Pause if no clients are listening
            if self.clients > 0:
                self.get_audio_chunk()

    def get_data(self):
        memory_file = BytesIO()
        wave_file = wave.open(memory_file, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

        memory_file.seek(0)
        data = memory_file.read()
        memory_file.close()

        self.frames.clear()
        
        return data

    def get_audio_chunk(self):
        ''' Get an audio chunk from internal stream '''
        raw_data = self.stream.read(CHUNK, exception_on_overflow=False)
        self.frames.append(raw_data)

    def close(self):
        ''' Close stream '''
        self.is_running = False
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
