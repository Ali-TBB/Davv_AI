"""module run_process"""

import json

import google.generativeai as genai

from src.base_model import BaseModel


class RunProcess(BaseModel):
    """
    Represents a process runner.

    Args:
        BaseModel: The base model class.

    Attributes:
        convo: The conversation object.
    """

    def __init__(self):
        super().__init__("dataset/data.json")

    def run(self, input_msg=None, path=None, type=None, mime_type=None):
        """
        Runs the process.

        Args:
            input_msg (str, optional): The input message. Defaults to None.
            path (str, optional): The file path. Defaults to None.
            type (str, optional): The type. Defaults to None.
            mime_type (str, optional): The MIME type. Defaults to None.
        """
        if path and type:
            upload_file = genai.upload_file(path, mime_type=mime_type)
            self.convo.send_message([input_msg, upload_file])
        else:
            self.convo.send_message(input_msg)
        output_msg = self.convo.last.text
        self.update_history(input_msg, output_msg, path, type)
        json_data = json.loads(self.split_output(output_msg))
        if json_data["action"] == "execute":
            if json_data["language"] == "python":
                self.run_command("command.py", json_data["code"])
        elif json_data["action"] == "response":
            response = json_data["response"]
            print(response)
