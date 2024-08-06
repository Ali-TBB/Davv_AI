from models.attachment import Attachment
from src.base_model import BaseModel
from src.data_types.divide_to_simple import DivideToSimpleDataType


class DivideToSimple(BaseModel):
    """
    A class that represents the DivideToSimple model.


    Methods:
        __init__(self): Initializes the DivideToSimple object.
        run(self, input_msg=None, path=None, type=None, mime_type=None): Runs the model with the given input.
        create_file(self, file_name, code): Creates a file with the given name and code.
        open_file(self, file_name): Opens the file with the given name.
    """

    backup_name = "divide_to_simple"
    data_type = DivideToSimpleDataType

    def handle_output(self, input_msg, output_msg, attachments: list[Attachment] = []):
        self.update_history(input_msg, output_msg, attachments)
        json_data = self.parse_output(output_msg)
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
