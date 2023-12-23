from PyQt5.QtCore import QObject, QThread, pyqtSignal
from .qqtSignalWrapper import qqtSignalWrapper

MAX_THREADS = 1000

class qqtThread(QThread):
    '''
    qqtThread is a wrapper for QThread.
    '''
    threadSignal = pyqtSignal(object)
    quitSignal = pyqtSignal(object)

    def __init__(self, args: list, id: int):
        QThread.__init__(self)
        self.func = args[0]
        self.id = id
        if len(args) > 1:
            self.args = args[1:]
        else:
            self.args = []

    def run(self):
        self.Run()

    def Run(self):
        if self.args != []:
            r = self.func(*self.args)
        else:
            r = self.func()
        self.threadSignal.emit(r)
        self.quitSignal.emit(self.id)

    def throw(self):
        self.wait()
        self.terminate()
        self.deleteLater()

class qqtThreadWrapper(QThread):
    '''
    qqtThreadWrapper is a thread manager.
    '''
    def __init__(self):
        QThread.__init__(self)
        self.threads = {}        

    def manageThread(self, funcName):
        if funcName in self.threads:
            self.threads[funcName].throw()
            self.threads.pop(funcName)

    def getInstance(self, variables, target):
        className = target.__qualname__.split(".")[0]
        for var in variables.values():
            if type(var).__name__ == className:
                return var
        return self

    def future(*args, **kwargs): # pylint: disable=E0213
        '''
        Decorator for threads.
        '''
        def decorator(func):
            def wrap(self, *_args):
                targetSelf = self.getInstance(vars(self), kwargs["target"])
                if "callback" in kwargs:
                    callbackSelf = self.getInstance(vars(self), kwargs["callback"])
                funcArgs = [kwargs["target"]]
                funcArgs.append(targetSelf)
                funcArgs.extend(_args)
                t = qqtThread(funcArgs, func.__name__)
                if "callback" in kwargs:
                    t.threadSignal.connect(getattr(callbackSelf, kwargs["callback"].__name__))
                t.quitSignal.connect(self.manageThread)
                self.threads[func.__name__] = t
                t.start()
            wrap.__name__ = func.__name__
            return wrap
        return decorator

class qqtThreadEscape(QObject):
    threadSignals = [qqtSignalWrapper() for _ in range(MAX_THREADS)]

    def __init__(self):
        QObject.__init__(self)
        for i in range(MAX_THREADS):
            self.threadSignals[i].threadSignal.connect(self.dispatch)

    def dispatch(self, func, *args):
        func(self, *(args[0]))

    def escape_thread(func):
        def decorator(self, *args):
            id = int(QThread.currentThreadId()) % MAX_THREADS
            self.threadSignals[id].threadSignal.emit(func, args)
        return decorator