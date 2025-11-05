from inspect import signature
from json import loads
from PyQt5.QtCore import pyqtSlot
from .qqtDebug import qqtDebug
from .qqtThread import qqtThreadWrapper as TW

class qqtCallback(TW):
    '''
    qqtCallback is a wrapper for callbacks.
    '''
    callbacks = {}

    @classmethod
    def register(cls, callback):
        '''
        Register a callback.
        '''
        name = callback.__name__
        cls.callbacks[name] = callback
        qqtDebug()(name, callback)
        return callback

    def call(self, name, args):
        '''
        Call a callback.
        '''
        qqtDebug()(name)
        if name in self.callbacks:
            try:
                self.callbacks[name](self, *loads(args))
            except RuntimeError as e:
                qqtDebug("e")("Args:", args)
                qqtDebug("e")("Signature:", signature(self.callbacks[name]))
                qqtDebug("e")("Parameters:", self.callbacks[name].__code__.co_varnames[1:])
                qqtDebug("e")(e)
        else:
            qqtDebug()("Callback not found", name)

    @pyqtSlot(str, str, name="call")
    @TW.future(target=call)
    def future_call(self, name, args): pass

def qcallback(func):
    '''
    Decorator for callbacks.
    '''
    return qqtCallback.register(func)
