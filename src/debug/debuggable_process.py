from multiprocessing import Process
from ptvsd import enable_attach, wait_for_attach
import sys

class DebuggableProcess(Process):
    '''
        A base class for debuggable processes
        Uses ptvsd
    '''
    def __init__(self):
        super(DebuggableProcess, self).__init__()

    def enable_logging(self, name):
        sys.stdout = open(name + '.out', 'a', buffering=0)
        sys.stderr = open(name + '_error.out', 'a', buffering=0)

    def enable_debug(self, port=5678):
        enable_attach(address=('0.0.0.0', port), redirect_output=True)
        wait_for_attach()