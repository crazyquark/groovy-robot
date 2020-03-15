from multiprocessing import Queue

from debug.debuggable_process import DebuggableProcess
from .mic_capture import MicCapture, MAX_FRAMES


class AudioProcess(DebuggableProcess):
    def __init__(self, queue):
        super(AudioProcess, self).__init__()
        self.queue = queue

    def run(self):
        # self.enable_debug(port=1234)
        self.enable_logging('microphone')

        mic = MicCapture()

        while True:
            frame = mic.queue.get()

            if self.queue.full():
                while not self.queue.empty():
                    try:
                        self.queue.get_nowait()
                    except:
                        # empty queue error
                        break
            try:
                self.queue.put_nowait(frame)
            except:
                # full exception happens because empty and full are unreliable
                continue

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
