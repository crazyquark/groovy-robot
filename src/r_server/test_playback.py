import pyaudio
import wave
import time

from mic_capture import CHANNELS, FORMAT, RATE, CHUNK

wf = wave.open('test.wav', 'rb')

def stream_callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

audio = pyaudio.PyAudio()
stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()), 
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        output_device_index = 3, # bluealsa please
                        stream_callback=stream_callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()
audio.terminate()