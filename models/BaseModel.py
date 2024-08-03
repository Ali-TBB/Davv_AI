#!/usr/bin/python3
import os
from FileHistory import ChatHistoryHandler
import google.generativeai as genai

def create_model():
    """
    Creates and configures the generative model.

    Returns:
        genai.GenerativeModel: The configured generative model.
    """
    # Read the API key from the file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_key_path = os.path.join(current_dir, "dataset/API_KEY")
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()

    # Configure the model with the API key
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain",
    }

    safety_settings = ChatHistoryHandler("dataset/safety_setting.json").history

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return model


class BaseModel():
    def __init__(self, JPath, filename, model):
        """
        Initializes a BaseModel instance.

        Args:
            JPath (str): The path to the J file.
            filename (str): The name of the file to save the command to.
            model (genai.GenerativeModel): The generative model to use.
        """
        self.JPath = JPath
        self.filename = filename
        self.model = model


    def save_command(self, command_content):
        """
        Saves the command content to a file.

        Args:
            command_content (str): The content of the command to save.
        """
        try:
            # Write command content to a temporary Python script
            with open(self.filename, "w") as file:
                file.write(command_content)
            # print(f"Command saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving the command: {e}")

    def Split_output(self, input_str):
        """
        Splits the input string and saves the code block to a file.

        Args:
            input_str (str): The input string to split.

        Returns:
            bool: True if code block is found and saved, False otherwise.
        """
        code_start_index = input_str.find("#code")
        if code_start_index != -1: # Found code
            start_index = input_str.find("```", code_start_index)
            end_index = input_str.find("```", start_index + 3)
            if start_index != -1 and end_index != -1:
                code_block = input_str[start_index:end_index + 3]
                code = code_block.replace("```python\n", "")
                code = code.replace("```", "")
                if code:
                    self.save_command(code)
                    return True # Found code
                else:
                    print("No code to save.")
        else:
            BLUE = '\033[94m'
            RESET = '\033[0m'
            print(f"{BLUE}{input_str}{RESET}")
            return False # No code found
