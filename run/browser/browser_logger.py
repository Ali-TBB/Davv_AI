from models.message import Message
from utils.logger import Logger


class BrowserLogger(Logger):

    __eel = None

    def __init__(self, eel):
        self.__eel = eel

    def log(self, level: str, message: str | Message):
        if isinstance(message, Message):
            self.__eel.messageReceived(message.data)
        else:
            self.__eel.log(level, message)
