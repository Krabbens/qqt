from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import sys, os
from colorama import just_fix_windows_console
from .qqtDebug import qqtDebug
from .qqtThread import qqtThreadWrapper
from .qqtCallback import qqtCallback
from .qqtConnector import qqtConnector
from PyQt5.QtCore import QThread

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
just_fix_windows_console()

class qqtApp(qqtThreadWrapper):
    def __init__(self):
        super().__init__()
        qqtDebug.main_thread_id = int(QThread.currentThreadId())
        qqtDebug()("qqtApp.__init__")
        self.app = QGuiApplication(sys.argv)
        self.callback = qqtCallback()
        self.connector = qqtConnector()

    def init(self):
        self.engine = QQmlApplicationEngine()
        ctx = self.engine.rootContext()
        ctx.setContextProperty('callback', self.callback)
        self.engine.load(os.path.join(os.path.dirname(sys.argv[0]), "main.qml"))
        qqtConnector.root = self.engine.rootObjects()[0]
        
    def run(self):
        self.init()
        sys.exit(self.app.exec())