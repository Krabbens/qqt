from PyQt5.QtCore import pyqtSlot
from .qqtDebug import qqtDebug
from .qqtThread import qqtThreadWrapper as TW
from inspect import signature
from json import loads

class qqtCallback(TW):
    callbacks = {}

    @classmethod
    def register(cls, callback):
        name = callback.__name__
        cls.callbacks[name] = callback
        qqtDebug()(name, callback)
        return callback

    def call(self, name, args):
        qqtDebug()(name)
        if name in self.callbacks:
            try:   
                self.callbacks[name](self, *loads(args))
            except Exception as e:
                qqtDebug("e")("Args:", args)
                qqtDebug("e")("Signature:", signature(self.callbacks[name]))
                qqtDebug("e")("Parameters:", self.callbacks[name].__code__.co_varnames[1:])
                qqtDebug("e")(e)
        else:
            qqtDebug()("Callback not found", name)

    @pyqtSlot(str, str, name="call")
    @TW.future(target=call)
    def future_call(self, name, args): pass
    
def qcallback(self):
    qqtDebug()(self)
    def _callback(func):
        return qqtCallback.register(func)
    _callback(self)