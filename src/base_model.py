import json
import subprocess

import google.generativeai as genai

from models.attachment import Attachment
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from utils.env import Env
from utils.storage import Directory, File


def create_model(mim_type, model_type, data_type, **kwargs):
    """
    Creates and configures the generative model.

    Args:
        mim_type (str): The MIME type of the response.
        model_type (str): The type of the generative model.

    Returns:
        genai.GenerativeModel: The configured generative model.
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
    Represents a base model for executing commands and managing chat history.

    Attributes:
        model (genai.GenerativeModel): The generative model to use.
        convo (genai.Conversation): The conversation object for chat history.
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
        """
        self.dataset = dataset
        self.directory = directory
        self.create_model()

    @property
    def backup(self) -> Dataset:
        """
        Backs up the chat history.
        """
        if self.backup_name:
            return Dataset.findWhere("`name` = ?", (self.backup_name,))

    def create_model(self):
        self.model = create_model(
            "application/json", "gemini-1.5-flash-latest", self.data_type
        )

        history = []
        backup_dataset = self.backup
        # all_items = (
        #     backup_dataset.all_items if backup_dataset else []
        # ) + self.dataset.all_items
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
        Updates the chat history with the input and output messages.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            path (str): The path associated with the message.
            type (str): The type of the message.
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
        raise NotImplementedError("Subclasses must implement this method")

    def parse_output(self, output):
        """
        Splits the output string and returns the JSON data.

        Args:
            output (str): The output string to split.

        Returns:
            str: The JSON data extracted from the output.
        """
        try:
            return json.loads(output)
        except:
            return {"response": output}

    def save_command(self, file_name, command_content):
        """
        Saves the command content to a file.

        Args:
            file_name (str): The name of the file to save the command to.
            command_content (str): The content of the command to save.
        """
        try:
            # Write command content to a temporary Python script
            file: File = self.directory.file(file_name)
            file.set(command_content)
            return file.path

            # print(f"Command saved to {file_name}")
        except Exception as e:
            print(f"An error occurred while saving the command: {e}")

    def run_command(self, file_name, code):
        """
        Runs the command by saving it to a file and executing it.

        Args:
            file_name (str): The name of the file to save the command to.
            code (str): The code to execute.
        """
        path = self.save_command(file_name, code)
        print("Operation is running ...")
        # Execute the command using subprocess
        result = subprocess.run(["python", path], capture_output=True)
        # Check the return code of the subprocess
        if result.returncode != 0:
            print(f"Command execution failed with return code {result.returncode}")
            # If there is an error, pass it to the Error method
            return self.fix_error(result.stderr.decode("utf-8"))
        else:
            # Print the output of the executed script
            RED = "\033[91m"
            RESET = "\033[0m"
            return "Output:\n" + RED + result.stdout.decode("utf-8") + RESET

    def fix_error(self, issue):
        """
        Fixes the error by running the error fixer.

        Args:
            issue (str): The error message.
        """
        from src.fix_error import FixError

        fixer = FixError(f"fix issue: {issue}", self.directory)
        return fixer.send_message(issue)
