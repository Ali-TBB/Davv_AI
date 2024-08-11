import json
import os
import subprocess

import google.generativeai as genai

from models.attachment import Attachment
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from utils.env import Env
from utils.storage import Directory, File


def create_model(mim_type, model_type, data_type, **kwargs):
    """
    Create a generative model with the specified configuration.

    Args:
        mim_type (str): The MIME type of the response.
        model_type (str): The type of the generative model.
        data_type (str): The schema of the response data.
        **kwargs: Additional keyword arguments for configuring the model.

    Returns:
        genai.GenerativeModel: The created generative model.
    """
    # Configure the model with the API key
    genai.configure(api_key=Env.get("API_KEY"))

    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        "response_mime_type": mim_type,
        "response_schema": data_type,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    model = genai.GenerativeModel(
        model_name=model_type,
        generation_config=generation_config,
        safety_settings=safety_settings,
        **kwargs,
    )

    return model


class BaseModel:
    """
    Base class for models in the AI system.

    Attributes:
        data_type (str): The type of data used by the model.
        dataset (Dataset): The dataset used by the model.
        directory (Directory): The directory where the model is stored.
        backup_name (str): The name of the backup dataset.
    """

    data_type = None
    dataset: Dataset
    directory: Directory

    backup_name: str = None

    def __init__(self, dataset: Dataset, directory: Directory):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            dataset (Dataset): The dataset used for training the model.
            directory (Directory): The directory where the model will be saved.
        """

        self.dataset = dataset
        self.directory = directory
        self.create_model()

    @property
    def backup(self) -> Dataset:
        """
        Backup the current dataset.

        Returns:
            Dataset: The backup dataset.
        """

        if self.backup_name:
            return Dataset.findWhere("`name` = ?", (self.backup_name,))

    def create_model(self):
        """
        Creates a model for the AI chatbot.

        This method initializes the model for the AI chatbot using the specified parameters.
        It also processes the history of conversation items, replacing attachment references
        with their corresponding URLs.

        Returns:
            None
        """

        self.model = create_model(
            "application/json", "gemini-1.5-flash-latest", self.data_type
        )

        history = []
        backup_dataset = self.backup
        all_items = backup_dataset.all_items if backup_dataset else []

        for dataset_item in all_items:
            history_item = {
                "role": dataset_item.role,
                "parts": dataset_item.parts,
            }

            i = 0
            for part in dataset_item.parts:
                if part.startswith("<-attachment->: "):
                    attachment_id = int(part.split("<-attachment->: ")[-1].strip())
                    attachment: Attachment = Attachment.find(attachment_id)
                    if attachment:
                        history_item["parts"][i] = attachment.url
                i += 1

            history.append(history_item)

        self.convo = self.model.start_chat(history=history)

    def update_history(self, input_msg, output_msg, attachments: list[Attachment] = []):
        """
        Update the history of the model with the input message, output message, and attachments.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            attachments (list[Attachment], optional): List of attachments. Defaults to [].
        """

        inputParts = [input_msg]
        for attachment in attachments:
            inputParts.append(f"<-attachment->: {attachment.id}")

        datasets_ids = [str(self.dataset.id)]
        if self.backup:
            datasets_ids.append(str(self.backup.id))

        exists = (
            DatasetItem.findWhere(
                f"`parts` = ? AND dataset_id IN ({', '.join([str(id) for id in datasets_ids])})",
                (json.dumps(inputParts),),
            )
            != None
        )

        if not exists:
            self.dataset.addItem("user", inputParts)

        self.dataset.addItem("model", [output_msg])

    def send_message(self, input_msg, attachments: list[Attachment] = []):
        """
        Sends a message to the conversation.

        Args:
            input_msg (str): The message to be sent.
            attachments (list[Attachment], optional): List of attachments to be sent with the message. Defaults to [].

        Returns:
            str: The output message received from the conversation.
        """

        if attachments:
            self.convo.send_message(
                [input_msg] + [attachment.url for attachment in attachments]
            )
        else:
            self.convo.send_message(input_msg)

        return self.handle_output(input_msg, self.convo.last.text, attachments)

    def handle_output(
        self, input_msg: str, output_msg: str, attachments: list[Attachment] = []
    ):
        """
        Handles the output of the model.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            attachments (list[Attachment], optional): List of attachments. Defaults to [].
        """

        raise NotImplementedError("Subclasses must implement this method")

    def parse_output(self, output):
        """
        Parses the output and returns a dictionary.

        Args:
            output (str): The output to be parsed.

        Returns:
            dict: The parsed output as a dictionary. If parsing fails, a dictionary with a single key "response" is returned,
                  with the value being the original output.
        """

        try:
            return json.loads(output)
        except:
            return {"response": output}

    def save_command(self, file_name, command_content, directory: Directory = None):
        """
        Saves the command content to a file in the specified directory.

        Args:
            file_name (str): The name of the file to save the command to.
            command_content (str): The content of the command to be saved.
            directory (Directory, optional): The directory to save the file in. If not provided, the default directory is used.

        Returns:
            str: The path of the saved file.

        Raises:
            Exception: If an error occurs while saving the command.
        """

        try:
            directory = directory or self.directory
            # Write command content to a temporary Python script
            file: File = directory.file(file_name)
            file.set(command_content)
            return file.path

            # print(f"Command saved to {file_name}")
        except Exception as e:
            print(f"An error occurred while saving the command: {e}")

    def run_command(self, file_name, code, directory: Directory = None, shell=False):
        """
        Executes a command by saving the code to a file, running it using subprocess,
        and returning the output.

        Args:
            file_name (str): The name of the file to save the code.
            code (str): The code to be executed.
            directory (Directory, optional): The directory where the file will be saved.
                If not provided, the default directory will be used.
            shell (bool, optional): Specifies whether to run the command in a shell.
                Defaults to False.

        Returns:
            str: The output of the executed script, or None if there is no output.

        Raises:
            Exception: If the command execution fails.

        """

        directory = directory or self.directory
        path = self.save_command(file_name, code, directory)
        print(path)
        os.chdir(directory.path)
        print("Operation is running ...")
        # Execute the command using subprocess
        result = subprocess.run(["start" if shell else "python", path], capture_output=True)
        os.chdir(Env.base_path)
        # Check the return code of the subprocess
        if result.returncode != 0:
            print(f"Command execution failed with return code {result.returncode}")
            # If there is an error, pass it to the Error method
            return self.fix_error(result.stderr.decode("utf-8"), directory)
        else:
            # Print the output of the executed script
            output = result.stdout.decode("utf-8")
            return output if output else None

    def fix_error(self, issue, directory: Directory = None):
        """
        Fixes the specified error by creating a FixError instance and sending a message.

        Args:
            issue (str): The issue to be fixed.
            directory (Directory, optional): The directory to fix the error in. If not provided, the default directory will be used.

        Returns:
            str: The response message from the FixError instance.

        """

        from src.fix_error import FixError

        fixer = FixError(f"fix issue: {issue}", directory or self.directory)
        return fixer.send_message(issue)
