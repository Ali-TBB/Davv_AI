import json
import subprocess

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

    def __init__(self):
        super().__init__("dataset/datafix.json")

    def run(self, input_msg):
        """
        Executes the error fixing process.

        Args:
            input_msg (str): The input message to be sent to the conversation.

        Returns:
            None
        """
        print("trying to fix the Error ...")
        self.convo.send_message(input_msg)
        output_msg = self.convo.last.text
        json_data = json.loads(self.split_output(output_msg))
        if json_data["action"] == "execute":
            if json_data["language"] == "python":
                self.save_command("ErrorCommand.py", json_data["code"])
                i = 0
                while (i < 3):
                    try:
                        # Execute the command using subprocess
                        result = subprocess.run(["python", "ErrorCommand.py"], capture_output=True)
                        # Check the return code of the subprocess
                        if result.returncode != 0:
                            print(f"Error Command execution failed with return code {result.returncode}")
                        else:
                            print("Error fixed, let's run it again ...")
                            return
                    except Exception as e:
                        print(f"An error occurred while running the command: {e}")
                    i += 1
                print("Error couldn't be fixed")
        elif json_data["action"] == "response":
            response =  json_data["response"]
            print(response)
