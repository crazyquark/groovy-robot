from audio import MicCapture, FORMAT, RATE, CHANNELS
import wave
from multiprocessing import Process

class P(Process):
    def __init__(self):
        super(P, self).__init__()

    def run(self):
        mic = MicCapture()
        wave_file = wave.open('test.wav', 'wb')
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(mic.audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)

        try:
            while True:
                if len(mic.frames) > 0:
                    print('Got ' + str(len(mic.frames)) + ' frames')
                    wave_file.writeframes(b''.join(mic.frames))
                    mic.frames.clear()
        except Exception as ex:
            print(ex)
        finally:
            print('Exiting...')
            mic.close()
            wave_file.close()

p = P()
p.start()
p.join()