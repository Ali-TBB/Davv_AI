import os
import subprocess

import google.generativeai as genai

from src.file_history import ChatHistoryHandler


def create_model(mim_type, model_type):
    """
    Creates and configures the generative model.

    Args:
        mim_type (str): The MIME type of the response.
        model_type (str): The type of the generative model.

    Returns:
        genai.GenerativeModel: The configured generative model.
    """
    # Read the API key from the file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_key_path = os.path.join(current_dir, "dataset/API_KEY")
    with open(api_key_path, "r") as file:
        api_key = file.read().strip()

    # Configure the model with the API key
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        "response_mime_type": mim_type,
    }

    safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_NONE"
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_NONE"
    }
  ]

    model = genai.GenerativeModel(
        model_name=model_type,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return model


class BaseModel:
    """
    Represents a base model for executing commands and managing chat history.

    Attributes:
        JPath (str): The path to the J file.
        model (genai.GenerativeModel): The generative model to use.
        convo (genai.Conversation): The conversation object for chat history.
    """

    def __init__(self, JPath):
        """
        Initializes a BaseModel instance.

        Args:
            JPath (str): The path to the J file.
        """
        self.JPath = JPath
        self.model = create_model("application/json", "gemini-1.5-pro-exp-0801")
        history_handler = self.Backup()
        self.convo = self.model.start_chat(history=history_handler.history)

    def save_command(self, file_name, command_content):
        """
        Saves the command content to a file.

        Args:
            file_name (str): The name of the file to save the command to.
            command_content (str): The content of the command to save.
        """
        try:
            # Write command content to a temporary Python script
            with open(file_name, "w") as file:
                file.write(command_content)
            # print(f"Command saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving the command: {e}")

    def split_output(self, output):
        """
        Splits the output string and returns the JSON data.

        Args:
            output (str): The output string to split.

        Returns:
            str: The JSON data extracted from the output.
        """
        json_data = output.replace("```json\n", "")
        json_data = json_data.replace("```", "")
        return json_data

    def update_history(self, input_msg, output_msg, path, type):
        """
        Updates the chat history with the input and output messages.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            path (str): The path associated with the message.
            type (str): The type of the message.
        """
        history_handler = ChatHistoryHandler(self.JPath)
        new_chat_entry = {"role": "user", "parts": ["{}".format(input_msg)]}
        if type:
            new_chat_entry["parts"].append(f"<-{type}->: {path}")
        new_chat_entry = {"role": "user", "parts": ["{}".format(input_msg)]}
        history_handler.update_history(new_chat_entry)
        new_chat_entry = {"role": "model", "parts": ["{}".format(output_msg)]}
        history_handler.update_history(new_chat_entry)
        history_handler.save_history()

    def Backup(self):
        """
        Backs up the chat history by uploading files.

        Returns:
            ChatHistoryHandler: The updated chat history handler.
        """
        history_handler = ChatHistoryHandler(self.JPath)
        i = 0
        for entry in history_handler.history:
            for part in entry["parts"]:
                if part.startswith("<-image->:"):
                    image_path = part.split("<-image->: ")[-1].strip()
                    upload_file = genai.upload_file(image_path, mime_type="image/png")
                    history_handler.history[i]["parts"][1] = upload_file
                if part.startswith("<-voice->:"):
                    voice_path = part.split("<-voice->: ")[-1].strip()
                    upload_file = genai.upload_file(voice_path, mime_type="voice/wav")
                    history_handler.history[i]["parts"][1] = upload_file
            i += 1
        return history_handler

    def run_command(self, file_name, code):
        """
        Runs the command by saving it to a file and executing it.

        Args:
            file_name (str): The name of the file to save the command to.
            code (str): The code to execute.
        """
        self.save_command(file_name, code)
        print("Operation is running ...")
        # Execute the command using subprocess
        result = subprocess.run(["python", self.filename], capture_output=True)
        # Check the return code of the subprocess
        if result.returncode != 0:
            print(f"Command execution failed with return code {result.returncode}")
            # If there is an error, pass it to the Error method
            self.fix_error(result.stderr.decode("utf-8"))
        else:
            # Print the output of the executed script
            RED = "\033[91m"
            RESET = "\033[0m"
            print("Output:\n", RED + result.stdout.decode("utf-8") + RESET)

    def fix_error(self, issue):
        """
        Fixes the error by running the error fixer.

        Args:
            issue (str): The error message.
        """
        from src.fix_error import FixError

        fixer = FixError()
        fixer.run(issue)
        # re run the command
        self.run(error_fixed=True)
