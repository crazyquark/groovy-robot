from multiprocessing import Process
from ptvsd import enable_attach, wait_for_attach

class DebuggableProcess(Process):
    '''
        A base class for debuggable processes
        Uses ptvsd
    '''
    def __init__(self):
        super(DebuggableProcess, self).__init__()
    
    def enable_debug(self, port=5678):
        enable_attach(redirect_output=True)
        wait_for_attach()