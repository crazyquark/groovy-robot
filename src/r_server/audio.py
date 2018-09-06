import pyaudio
import wave
from io import BytesIO
# import numpy

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 4096
RECORD_SECONDS = 5

class MicCapture:
    ''' Captures mic input as audio chunks '''

    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def get_audio_chunk(self):
        ''' Get an audio chunk from internal stream '''
        stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                 rate=RATE, input=True,
                                 input_device_index=2,
                                 frames_per_buffer=CHUNK)

        raw_data = stream.read(CHUNK)
        memory_file = BytesIO()

        wave_file = wave.open(memory_file, 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(raw_data)
        wave_file.close()

        memory_file.seek(0)
        data = memory_file.read()
        memory_file.close()

        stream.stop_stream()
        stream.close()

        return data

    def close(self):
        ''' Close stream '''
        self.audio.terminate()
