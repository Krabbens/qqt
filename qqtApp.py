import sys
import os
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QThread
from colorama import just_fix_windows_console
from .qqtDebug import qqtDebug
from .qqtThread import qqtThreadWrapper
from .qqtCallback import qqtCallback
from .qqtConnector import qqtConnector
from .qqtEngineManager import qqtEngineManager
from .qqtModel import qqtModel

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
just_fix_windows_console()

class qqtApp(qqtThreadWrapper):
    '''
    qqtApp is a wrapper for QGuiApplication and QQmlApplicationEngine.
    '''
    def __init__(self, entry_qml="main.qml"):
        super().__init__()
        qqtDebug.main_thread_id = int(QThread.currentThreadId())
        qqtDebug()("qqtApp.__init__")
        self.entry_qml = entry_qml
        self.engine = None
        self.app = QGuiApplication(sys.argv)
        self.callback = qqtCallback()
        self.connector = qqtConnector()
        self.create_engine()
        

    def create_engine(self):
        '''
        Create QQmlApplicationEngine.
        '''
        self.engine = QQmlApplicationEngine()
        qqtEngineManager.set_engine(self.engine)

    def init(self):
        '''
        Initialize QGuiApplication.
        '''
        ctx = self.engine.rootContext()
        ctx.setContextProperty('callback', self.callback)
        self.engine.load(os.path.join(os.path.dirname(sys.argv[0]), self.entry_qml))
        qqtConnector.root = self.engine.rootObjects()[0]
        
    def run(self):
        '''
        Run QGuiApplication.
        '''
        self.init()

        for obj in self.engine.rootObjects()[0].children():
            if obj.property("shadow") is not None:
                self.shadowModel.add_items([{"source": obj}])

        sys.exit(self.app.exec())