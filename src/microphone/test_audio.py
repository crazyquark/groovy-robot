from mic_capture import MicCapture, FORMAT, RATE, CHANNELS, SAMPLEWIDTH
import wave
from multiprocessing import Process, Queue

class P(Process):
    def __init__(self, q):
        super(P, self).__init__()
        self.q = q

    def run(self):
        mic = MicCapture()

        try:
            while True:
                if len(mic.frames) > 0:
                    frame = mic.frames.pop()
                    self.q.put(frame) 
        except Exception as ex:
            print(ex)
        finally:
            print('Exiting...')
            mic.close()

if __name__ == '__main__':  
    wave_file = wave.open('test.wav', 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(SAMPLEWIDTH)
    wave_file.setframerate(RATE)

    q = Queue()

    p = P(q)
    p.start()

    try:
        while True:
            if (not q.empty()):
                print('Received from queue')
                frame = q.get()
                wave_file.writeframes(frame)
    finally:
        wave_file.close()
        p.join()

