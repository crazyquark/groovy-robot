from multiprocessing import Queue

from debug.debuggable_process import DebuggableProcess
from .mic_capture import MicCapture, MAX_FRAMES
from flask_socketio import SocketIO

class AudioProcess(DebuggableProcess):
    def __init__(self):
        super(AudioProcess, self).__init__()
        self.socket = SocketIO(message_queue='redis://')
    def run(self):
        # self.enable_debug(port=1234)
        self.enable_logging('microphone')

        self.mic = MicCapture()

        while True:
            try:
                frame = self.mic.queue.get_nowait().tobytes()
                self.socket.emit('data', frame, namespace='/audio')
            except Exception as ex:
                # full exception happens because empty and full are unreliable
                # continue
                print(ex)

    @classmethod
    def start_capture(cls):
        # Singleton
        if hasattr(cls, 'instance'):
            return cls.queue

        # cls.queue = Queue(MAX_FRAMES)
        cls.instance = AudioProcess()
        cls.instance.daemon = True
        cls.instance.start()

    @classmethod
    def stop_capture(cls):
        if hasattr(cls, 'instance'):
            cls.instance.terminate()
