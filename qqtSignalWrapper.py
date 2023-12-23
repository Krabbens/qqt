'''module responsible for wrapping signals'''

from PyQt5.QtCore import QObject, pyqtSignal

class qqtSignalWrapper(QObject):
    '''
    qqtSignalWrapper is a wrapper for pyqtSignal.
    '''
    threadSignal = pyqtSignal(object, object)

    def __init__(self):
        QObject.__init__(self)