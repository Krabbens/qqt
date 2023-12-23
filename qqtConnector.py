from json import dumps
from .qqtThread import qqtThreadEscape as TE
from .qqtDebug import qqtDebug as D


class qqtConnector(TE):
    '''
    qqtConnector is a wrapper for QML.
    '''
    root = None

    @classmethod
    @TE.escape_thread
    def call(cls, name, args):
        '''
        Call a QML function.
        '''
        try:
            getattr(cls.root, name)(dumps(args))
        except RuntimeError as e:
            D("e")("Args:", args)
            D("e")(e)

def call_qml(name, args):
    '''
    Call a QML function.
    '''
    qqtConnector.call(name, args)