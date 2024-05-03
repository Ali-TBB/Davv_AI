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


class HelpFixError:
    def __init__(self, model, error_description):
        self.model = model
        self.error_description = error_description

    def suggest_fix(self):
        # Generate additional information or suggestions using the model
        conversation = self.model.start_chat(history=[{"role": "user", "parts": [self.error_description]}])
        return conversation.last.text

# Example usage:
"""
error_description = "I encountered an error while executing the code."
helper = HelpFixError(model, error_description)
suggestion = helper.suggest_fix()
print("Suggested Fix:", suggestion)

"""