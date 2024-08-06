from models.message import Message


class Logger:

    def log(self, level: str, message: str | Message):
        if isinstance(message, Message):
            print(message.text)
        else:
            print(f"[{level.upper()}] {message}")

    def info(self, message):
        self.log("info", message)

    def error(self, message):
        self.log("error", message)

    def message(self, message: Message):
        self.log("message", message)
