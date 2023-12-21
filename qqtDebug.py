import colorama
import sys
import inspect
from PyQt5.QtCore import QThread

class qqtDebug:
    main_thread_id = None

    def __init__(self, level="d"):
        self.debug = len(sys.argv) > 1 and "d" in sys.argv[1]
        self.is_worker = int(QThread.currentThreadId()) != self.main_thread_id
        self.colors = [
            colorama.Fore.LIGHTRED_EX,
            colorama.Fore.RED,
            colorama.Fore.BLUE,
            colorama.Fore.GREEN,
            colorama.Fore.RESET,
        ]
        self.level = "t" if self.is_worker and "t" and level != "e" in sys.argv[1] else level
        self.level = "p" if self.main_thread_id is None else self.level
        self.levels = {
            "p": colorama.Fore.LIGHTGREEN_EX + "[pre-start] ",
            "d" : colorama.Fore.LIGHTRED_EX + "[debug] ",
            "t" : colorama.Fore.LIGHTBLUE_EX + "[thread " + str(int(QThread.currentThreadId()))[:3] + "] ",
            "vv" : colorama.Fore.LIGHTYELLOW_EX + "[vv] ",
            "vvv" : colorama.Fore.RED + "[vvv] ",
            "e": colorama.Back.RED + colorama.Fore.WHITE + "[error]" + colorama.Fore.RESET + colorama.Back.RESET + " ",
        }

    def __call__(self, *args, **kwargs):
        if self.debug and self.level in sys.argv[1]:
            stack = inspect.stack()
            if "self" in stack[1][0].f_locals:
                caller_cls = stack[1][0].f_locals["self"].__class__.__name__
            else:
                caller_cls = "decorator"
            caller_method = stack[1][0].f_code.co_name
            print(
                self.levels[self.level]
                + self.colors[0]
                + caller_cls
                + self.colors[-1]
                + "."
                + self.colors[1]
                + caller_method
                + " ",
                end="",
            )
            for i in range(len(args) - 1):
                print(self.colors[i + 2] + str(args[i]), end=" ")
            print(self.colors[-1] + str(args[-1]), end="")
            print(colorama.Fore.RESET)