import pyaudio
import wave
import time
from io import BytesIO

FORMAT = pyaudio.paInt16
SAMPLEWIDTH = 2 # int16
CHANNELS = 1
RATE = 44100
CHUNK = 2048
MAX_FRAMES = 5

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK, stream_callback=self.stream_callback)

        self.frames = []
        self.stream.start_stream()

    def stream_callback(self, in_data, frame_count, time_info, status):
        ''' Get an audio chunk from internal stream '''
        self.frames.append(in_data)

        return (in_data, pyaudio.paContinue)

    @staticmethod
    def encode_data(raw_data):
        # convert current chunk    
        memory_file = BytesIO()
        wave_file = wave.open(memory_file, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(SAMPLEWIDTH)
        wave_file.setframerate(RATE)
        wave_file.writeframes(raw_data)
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
