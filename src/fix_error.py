import subprocess

from models.attachment import Attachment
from src.base_model import BaseModel


class FixError(BaseModel):
    """
    Class to fix errors in the dataset.

    Attributes:
        None

    Methods:
        __init__(self): Initializes the FixError class.
        run(self, input_msg): Runs the error fixing process.

    """

    backup_name = "fix_error"

    def handle_output(self, input_msg, output_msg, attachments: list[Attachment] = []):
        json_data = self.parse_output(output_msg)
        if json_data["action"] == "execute":
            if json_data["language"] == "python":
                path = self.save_command("ErrorCommand.py", json_data["code"])
                i = 0
                while i < 3:
                    try:
                        # Execute the command using subprocess
                        result = subprocess.run(["python", path], capture_output=True)
                        # Check the return code of the subprocess
                        if result.returncode != 0:
                            print(
                                f"Error Command execution failed with return code {result.returncode}"
                            )
                        else:
                            return "Error fixed, let's run it again ..."
                    except Exception as e:
                        print(f"An error occurred while running the command: {e}")
                    i += 1
                return "Error couldn't be fixed"
        elif "response" in json_data:
            return json_data["response"]
        else:
            return f"Invalid command {json_data['action']}."
