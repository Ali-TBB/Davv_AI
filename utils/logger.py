from models.message import Message


class Logger:
    """
    A class for logging messages at different levels.

    Methods:
    - log(level: str, message: str | Message): Logs the message at the specified level.
    - info(message): Logs the message at the 'info' level.
    - error(message): Logs the message at the 'error' level.
    - message(message: Message): Logs the message at the 'message' level.
    - window_down(): Placeholder method for window down action.
    - window_up(): Placeholder method for window up action.
    """

    def log(self, level: str, message: str | Message):
        """
        Logs a message with the specified level.

        Args:
            level (str): The log level.
            message (str | Message): The message to be logged. If a Message object is provided, its text will be printed.

        Returns:
            None
        """

        if isinstance(message, Message):
            print(message.text)
        else:
            print(f"[{level.upper()}] {message}")

    def info(self, message):
        """
        Logs an informational message.

        Args:
            message (str): The message to be logged.
        """

        self.log("info", message)

    def error(self, message):
        """
        Logs an error message.

        Args:
            message (str): The error message to be logged.
        """

        self.log("error", message)

    def message(self, message: Message):
        """
        Logs a message.

        Args:
            message (Message): The message to be logged.
        """

        self.log("message", message)

    def window_down(self):
        """
        Lowers the window down.
        """

        pass

    def window_up(self):
        """
        Raises the window up.
        """

        pass
