import webview

from models.message import Message
from utils.logger import Logger


class BrowserLogger(Logger):
    """
    A class that provides logging functionality for the browser.

    Args:
        eel: The Eel instance used for communication with the frontend.

    Attributes:
        __eel: The Eel instance used for communication with the frontend.
    """

    __eel = None

    def __init__(self, eel):
        """
        Initializes the BrowserLogger object.

        Args:
            eel: The eel object used for communication with the browser.
        """

        self.__eel = eel

    def log(self, level: str, message: str | Message):
        """
        Logs a message with the specified level.

        Args:
            level (str): The log level.
            message (str | Message): The message to be logged. It can be a string or a Message object.
        """

        if isinstance(message, Message):
            self.__eel.messageReceived(message.__dict__())
        else:
            self.__eel.log(level, message)

    def window_down(self):
        """
        Minimizes the browser window.
        """

        # webview.windows[0].minimize()
        pass

    def window_up(self):
        """
        Restores the browser window.
        """

        # webview.windows[0].restore()
        pass
