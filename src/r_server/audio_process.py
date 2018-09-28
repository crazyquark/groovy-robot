from multiprocessing import Process, Queue

from .mic_capture import MicCapture, MAX_FRAMES

class AudioProcess(Process):
    def __init__(self, queue):
        super(AudioProcess, self).__init__()
        self.queue = queue

    def run(self):
        mic = MicCapture()

        while True:
            if len(mic.frames) > 0:
                frame = mic.frames.pop()
                
                # Make room in the queue
                if self.queue.full():
                    while not self.queue.empty():
                        self.queue.get_nowait()

                self.queue.put_nowait(frame)

    @classmethod
    def start_capture(cls):
        # Singleton
        if hasattr(cls, 'instance'):
            return cls.queue
        
        cls.queue = Queue(MAX_FRAMES)
        cls.instance = AudioProcess(cls.queue)
        cls.instance.start()

        return cls.queue

    @classmethod
    def stop_capture(cls):
        if hasattr(cls, 'instance'):
            cls.instance.terminate()