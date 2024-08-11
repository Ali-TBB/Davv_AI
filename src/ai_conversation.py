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
from src.divide_to_simple import DivideToSimple
from src.find_requirements import FindRequirements
from src.run_process import RunProcess


class AIConversation(Conversation):
    """
    AIConversation class represents a conversation with an AI model.

    Attributes:
        __logger (Logger): The logger object for logging messages.
        __run_process (RunProcess): The RunProcess object for running processes.
        __find_requirement (FindRequirements): The FindRequirements object for finding requirements.
        __divide_to_simple (DivideToSimple): The DivideToSimple object for dividing complex tasks into simpler ones.

    Methods:
        __init__: Initializes an AIConversation object.
        init: Initializes the RunProcess, FindRequirements, and DivideToSimple objects.
        directory: Returns the directory associated with the conversation.
        logger: Returns the logger object.
        run_process: Returns the RunProcess object.
        find_requirement: Returns the FindRequirements object.
        divide_to_simple: Returns the DivideToSimple object.
        handle_message: Handles a message in the conversation.
        take_screenshot: Takes a screenshot and saves it as an attachment.
        new: Creates a new AIConversation object.

    """

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
        """
        Initializes an AIConversation object.

        Args:
            id (int): The ID of the conversation.
            name (str): The name of the conversation.
            dataset_id (int): The ID of the dataset associated with the conversation.
            created_at (optional): The creation timestamp of the conversation.
            updated_at (optional): The last updated timestamp of the conversation.
            logger (Logger, optional): The logger object for logging messages.

        """

        super().__init__(id, name, dataset_id, created_at, updated_at)
        self.__logger = logger

    def init(self):
        """
        Initializes the RunProcess, FindRequirements, and DivideToSimple objects.

        """

        self.__run_process = RunProcess(self.dataset, self.directory)
        self.__find_requirement = FindRequirements(self.dataset, self.directory)
        self.__divide_to_simple = DivideToSimple(self.dataset, self.directory)

    @property
    def directory(self) -> Directory:
        """
        Returns the directory associated with the conversation.

        Returns:
            Directory: The directory object.

        """

        return get_storage().directory(f"conv-{self.id}")

    @property
    def logger(self) -> Logger:
        """
        Returns the logger object.

        Returns:
            Logger: The logger object.

        """

        return self.__logger

    @property
    def run_process(self) -> RunProcess:
        """
        Returns the RunProcess object.

        Returns:
            RunProcess: The RunProcess object.

        """

        return self.__run_process

    @property
    def find_requirement(self) -> FindRequirements:
        """
        Returns the FindRequirements object.

        Returns:
            FindRequirements: The FindRequirements object.

        """

        return self.__find_requirement

    @property
    def divide_to_simple(self) -> DivideToSimple:
        """
        Returns the DivideToSimple object.

        Returns:
            DivideToSimple: The DivideToSimple object.

        """

        return self.__divide_to_simple

    def handle_message(
        self, message_content, attachments: list[Attachment] = []
    ) -> Message:
        """
        Handles a message in the conversation.

        Args:
            message_content: The content of the message.
            attachments (list[Attachment], optional): The list of attachments.

        Returns:
            Message: The message object.

        """

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
        """
        Takes a screenshot and saves it as an attachment.

        Returns:
            Attachment: The screenshot attachment.

        """

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
        """
        Creates a new AIConversation object.

        Args:
            name (str): The name of the conversation.
            **kwargs: Additional keyword arguments.

        Returns:
            AIConversation: The new AIConversation object.

        """

        dataset = Dataset.create(None, "Conversation dataset - " + name)
        return cls.create(None, name, dataset.id, **kwargs)
