from BaseModel import BaseModel
import subprocess

class FixError(BaseModel):
    def __init__(self, value):
        super().__init__("dataset/datafix.json", value, "ErrorCommand.py")

    def Run(self):
        print("trying to fix the Error ...")
        try:
            # Execute the command using subprocess
            result = subprocess.run(["python", "ErrorCommand.py"], capture_output=True)
            # Check the return code of the subprocess
            if result.returncode != 0:
                print(f"Error Command execution failed with return code {result.returncode}")
            else:
                print("Error fixed, let's run it again ...")
        except Exception as e:
            print(f"on fix An error occurred while running the command: {e}")

