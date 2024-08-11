import os
import time
from models.attachment import Attachment
from src.base_model import BaseModel
from src.data_types.divide_to_simple import DivideToSimpleDataType
from utils.storage import Directory


class DivideToSimple(BaseModel):
    """
    This class represents the DivideToSimple model.

    Attributes:
        backup_name (str): The name of the backup.
        data_type (DivideToSimpleDataType): The data type of the model.
        project_dir (Directory): The project directory.
    """

    backup_name = "divide_to_simple"
    data_type = DivideToSimpleDataType

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_dir = self.directory.directory(
            f"project-{time.strftime('%Y%m%d-%H%M%S')}"
        )

    def handle_output(
        self, input_msg: str, output_msg: str, attachments: list[Attachment] = []
    ):
        """
        Handles the output of the model.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            attachments (list[Attachment], optional): The list of attachments. Defaults to [].

        Returns:
            str: The result message.
        """

        self.update_history(input_msg, output_msg, attachments)
        json_data = self.parse_output(output_msg)
        for step in json_data["steps"]:
            if step["action"] == "create_file":
                self.create_file(step["file_name"], step["code"])
            if step["action"] == "run_command":
                if step["language"] == "python":
                    self.run_command("run.py", step["code"], self.project_dir)
                elif step["language"] == "shell":
                    import platform

                    ext = {"Windows": "bat", "Linux": "sh"}[platform.system()]
                    self.run_command(
                        f"run.{ext}", step["code"], self.project_dir, shell=True
                    )
            if step["action"] == "open_file":
                self.open_file(step["file_name"])
        return "Done"

    def create_file(self, file_name, code):
        """
        Creates a file with the given name and code.

        Args:
            file_name (str): The name of the file.
            code (str): The code to be written in the file.
        """

        project_path = self.project_dir.path
        try:
            # Write command content to a temporary Python script
            with open(os.path.join(project_path, file_name), "w") as file:
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
