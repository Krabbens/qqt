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

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
just_fix_windows_console()

class qqtApp(qqtThreadWrapper):
    '''
    qqtApp is a wrapper for QGuiApplication and QQmlApplicationEngine.
    '''
    def __init__(self):
        super().__init__()
        qqtDebug.main_thread_id = int(QThread.currentThreadId())
        qqtDebug()("qqtApp.__init__")
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
        self.engine.load(os.path.join(os.path.dirname(sys.argv[0]), "main.qml"))
        qqtConnector.root = self.engine.rootObjects()[0]
        
    def run(self):
        '''
        Run QGuiApplication.
        '''
        self.init()
        sys.exit(self.app.exec())