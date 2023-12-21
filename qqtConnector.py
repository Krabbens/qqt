from .qqtThread import qqtThreadEscape as TE
from .qqtDebug import qqtDebug as D
from inspect import signature
from json import dumps

class qqtConnector(TE):
    root = None

    def __init__(self):
        super().__init__()

    @classmethod
    @TE.escape_thread
    def call(self, name, args):
        try:
            getattr(self.root, name)(dumps(args))
        except Exception as e:
            D("e")("Args:", args)
            D("e")(e)

def call_qml(name, args):
    qqtConnector.call(name, args)