import webview

from models.message import Message
from utils.logger import Logger


class BrowserLogger(Logger):

    __eel = None

    def __init__(self, eel):
        self.__eel = eel

    def log(self, level: str, message: str | Message):
        if isinstance(message, Message):
            self.__eel.messageReceived(message.__dict__())
        else:
            self.__eel.log(level, message)

    def window_down(self):
        webview.windows[0].minimize()

    def window_up(self):
        webview.windows[0].restore()
