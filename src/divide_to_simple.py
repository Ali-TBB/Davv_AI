import json

import google.generativeai as genai

from src.base_model import BaseModel


class DivideToSimple(BaseModel):
    """
    A class that represents the DivideToSimple model.

    Attributes:
        JPath (str): The path to the JSON dataset file.

    Methods:
        __init__(self): Initializes the DivideToSimple object.
        run(self, input_msg=None, path=None, type=None, mime_type=None): Runs the model with the given input.
        create_file(self, file_name, code): Creates a file with the given name and code.
        open_file(self, file_name): Opens the file with the given name.
    """

    def __init__(self):
        super().__init__(JPath="dataset/Data_Divide_to_sm.json")

    def run(self, input_msg=None, path=None, type=None, mime_type=None):
        """
        Runs the model with the given input.

        Args:
            input_msg (str): The input message.
            path (str): The path to the file.
            type (str): The type of the file.
            mime_type (str): The MIME type of the file.

        Returns:
            dict: The output data in JSON format.
        """
        if path and type:
            upload_file = genai.upload_file(path, mime_type=mime_type)
            self.convo.send_message([input_msg, upload_file])
        else:
            self.convo.send_message(input_msg)
        output_msg = self.convo.last.text
        self.update_history(input_msg, output_msg, path, type)
        json_data = json.loads(self.split_output(output_msg))
        for step_name in json_data:
            step = json_data[step_name]
            if step["action"] == "create_file":
                self.create_file(step["file_name"], step["code"])
            if step["action"] == "run_command":
                self.run_command("command.py", step["code"])
        return json_data

    def create_file(self, file_name, code):
        """
        Creates a file with the given name and code.

        Args:
            file_name (str): The name of the file.
            code (str): The code to be written in the file.
        """
        try:
            # Write command content to a temporary Python script
            with open(file_name, "w") as file:
                file.write(code)
            print(f"file created {file_name}")
        except Exception as e:
            print(f"An error occurred while saving the file {file_name}: {e}")

    def open_file(self, file_name):
        """
        Opens the file with the given name.

        Args:
            file_name (str): The name of the file.
        """
        pass
