from multiprocessing import Process
import sys

class DebuggableProcess(Process):
    '''
        A base class for debuggable processes
        Uses ptvsd
    '''
    def __init__(self):
        super(DebuggableProcess, self).__init__()
        self.daemon = True

    def enable_logging(self, name):
        sys.stdout = open(name + '.out', 'a')
        sys.stderr = open(name + '_error.out', 'a')
