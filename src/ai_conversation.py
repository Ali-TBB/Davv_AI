import os
import time

import pyautogui
import google.generativeai as genai

from models.attachment import Attachment
from models.conversation import Conversation
from models.dataset import Dataset
from models.message import Message
from utils.env import Env
from utils.logger import Logger
from utils.storage import Directory, get_storage
from src.base_model import BaseModel


class AIConversation(Conversation):

    __logger: Logger
    __run_process: BaseModel = None
    __find_requirement: BaseModel = None
    __divide_to_simple: BaseModel = None
    __directory: Directory = None

    def __init__(
        self,
        id: int,
        name: str,
        dataset_id: int,
        created_at=None,
        updated_at=None,
        logger: Logger = None,
    ):
        super().__init__(id, name, dataset_id, created_at, updated_at)
        self.__logger = logger
        self.__directory = get_storage().directory(f"conv-{self.id}")

    @property
    def logger(self) -> Logger:
        return self.__logger

    @property
    def directory(self) -> Directory:
        return self.__directory

    @property
    def run_process(self):
        from src.run_process import RunProcess

        if not self.__run_process:
            self.__run_process = RunProcess(self.dataset, self.directory)
        return self.__run_process

    @property
    def find_requirement(self):
        from src.find_requirements import FindRequirements

        if not self.__find_requirement:
            self.__find_requirement = FindRequirements(self.dataset, self.directory)
        return self.__find_requirement

    @property
    def divide_to_simple(self):
        from src.divide_to_simple import DivideToSimple

        if not self.__divide_to_simple:
            self.__divide_to_simple = DivideToSimple(self.dataset, self.directory)
        return self.__divide_to_simple

    def handle_message(self, message, attachments: list[Attachment] = []) -> Message:
        self.sendMessage("user", message)

        result, input_msg = self.find_requirement.send_message(message, attachments)
        if result == "screenshot":
            attachments.append(self.take_screenshot())
            answerContent = self.run_process.send_message(message, attachments)
        elif result == "simple":
            answerContent = self.run_process.send_message(message, attachments)
        elif result == "big":
            answerContent = self.divide_to_simple.send_message(message, attachments)
        elif result == "response":
            answerContent = input_msg
        else:
            answerContent = "Invalid command."

        return self.sendMessage("model", answerContent)

    def take_screenshot(self) -> Attachment:
        full_path = self.directory.file(f"{time.strftime('%y_%m_%d_%H%M%S')}.png").path
        # Capture the screenshot
        screenshot = pyautogui.screenshot()
        # Save the screenshot to the specified file path
        screenshot.save(full_path)
        self.__logger.info("Screenshot saved successfully!")
        attachment = Attachment(None, "image/png", full_path)
        Attachment.create(attachment)
        return attachment

    @classmethod
    def new(cls, name: str, **kwargs) -> "AIConversation":
        dataset = Dataset.create(None, "Conversation dataset - " + name)
        return cls.create(None, name, dataset.id, **kwargs)
