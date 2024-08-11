import json
import os
import time

import pyautogui

from models.attachment import Attachment
from models.conversation import Conversation
from models.dataset import Dataset
from models.message import Message
from utils.logger import Logger
from utils.storage import Directory, get_storage
from src.base_model import BaseModel
from src.divide_to_simple import DivideToSimple
from src.find_requirements import FindRequirements
from src.run_process import RunProcess


class AIConversation(Conversation):

    __logger: Logger
    __run_process: RunProcess = None
    __find_requirement: FindRequirements = None
    __divide_to_simple: DivideToSimple = None

    def __init__(
        self,
        id: int,
        name: str,
        dataset_id: int,
        created_at=None,
        updated_at=None,
        logger: Logger = Logger(),
    ):
        super().__init__(id, name, dataset_id, created_at, updated_at)
        self.__logger = logger

    def init(self):
        self.__run_process = RunProcess(self.dataset, self.directory)
        self.__find_requirement = FindRequirements(self.dataset, self.directory)
        self.__divide_to_simple = DivideToSimple(self.dataset, self.directory)

    @property
    def directory(self) -> Directory:
        return get_storage().directory(f"conv-{self.id}")

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def run_process(self) -> RunProcess:
        return self.__run_process

    @property
    def find_requirement(self) -> FindRequirements:
        return self.__find_requirement

    @property
    def divide_to_simple(self) -> DivideToSimple:
        return self.__divide_to_simple

    def handle_message(
        self, message_content, attachments: list[Attachment] = []
    ) -> Message:
        message = self.send_message(
            "user", message_content, [a.id for a in attachments]
        )

        result, input_msg = self.find_requirement.send_message(
            message_content, attachments
        )
        print("result: ", result, "msg: ", input_msg)
        if result == "screenshot":
            screenshot = self.take_screenshot()
            attachments.append(screenshot)
            message.add_attachment(screenshot)

            answer, output = self.run_process.send_message(message_content, attachments)
        elif result == "simple":
            answer, output = self.run_process.send_message(message_content, attachments)
        elif result == "big":
            answer = self.divide_to_simple.send_message(message_content, attachments)
        elif result == "response":
            answer = input_msg
        else:
            answer = "Invalid command."

        return message, self.send_message(
            "model", json.loads(answer) if type(answer) != str else answer
        )

    def take_screenshot(self) -> Attachment:
        filename = f"{time.strftime('%y_%m_%d_%H%M%S')}.png"
        file = self.directory.file(filename)

        # self.logger.window_down()
        screenshot = pyautogui.screenshot()
        screenshot.save(file.path)
        # self.logger.window_up()

        self.logger.info("Screenshot saved successfully!")

        return Attachment.create(
            None, "image/png", os.path.join(self.directory.name, file.name)
        )

    @classmethod
    def new(cls, name: str, **kwargs) -> "AIConversation":
        dataset = Dataset.create(None, "Conversation dataset - " + name)
        return cls.create(None, name, dataset.id, **kwargs)
