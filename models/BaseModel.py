#!/usr/bin/python3
import os
import subprocess
from FileHistory import ChatHistoryHandler
import google.generativeai as genai

def create_model(mim_type, model_type):
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
        "response_mime_type": mim_type,
    }

    safety_settings = ChatHistoryHandler("dataset/safety_setting.json").history

    model = genai.GenerativeModel(
        model_name=model_type,
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return model


class BaseModel():
    def __init__(self, JPath, filename= None):
        """
        Initializes a BaseModel instance.

        Args:
            JPath (str): The path to the J file.
            filename (str): The name of the file to save the command to.
            model (genai.GenerativeModel): The generative model to use.
        """
        self.JPath = JPath
        self.filename = filename

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

    def split_output(self, output):
        json_data = output.replace("```json\n", "")
        json_data = json_data.replace("```", "")
        return json_data

    def update_history(self, input_msg, output_msg, image_path, voice_path):
        history_handler = ChatHistoryHandler(self.JPath)
        if image_path:
            new_chat_entry = {"role": "user", "parts": ["{}".format(input_msg), f"image : {image_path}"]}
        elif voice_path:
            new_chat_entry = {"role": "user", "parts": ["{}".format(input_msg), f"voice : {voice_path}"]}
        new_chat_entry = {"role": "user", "parts": ["{}".format(input_msg)]}
        history_handler.update_history(new_chat_entry)
        new_chat_entry = {"role": "model", "parts": ["{}".format(output_msg)]}
        history_handler.update_history(new_chat_entry)
        history_handler.save_history()


    def Backup(self):
        history_handler = ChatHistoryHandler(self.JPath)
        i = 0
        for entry in history_handler.history:
            for part in entry["parts"]:
                if "image :" in part:
                    image_path = part.split("image : ")[-1].strip()
                    upload_file = genai.upload_file(image_path, mime_type="image/png")
                    history_handler.history[i]["parts"][1] = upload_file
                if "voice :" in part:
                    voice_path = part.split("voice : ")[-1].strip()
                    upload_file = genai.upload_file(voice_path, mime_type="voice/wav")
                    history_handler.history[i]["parts"][1] = upload_file 
            i += 1
        return history_handler

    def Run_command(self):
        print("Operation is running ...")
        try:
            # Execute the command using subprocess
            result = subprocess.run(["python", self.filename], capture_output=True)
            # Check the return code of the subprocess
            if result.returncode != 0:
                print(f"Command execution failed with return code {result.returncode}")
                # If there is an error, pass it to the Error method
                self.Error(result.stderr.decode("utf-8"))
            else:
                # Print the output of the executed script
                RED = '\033[91m'
                RESET = '\033[0m'
                print("Output:\n", RED + result.stdout.decode("utf-8") + RESET)
        except Exception as e:
            print(f"on run An error occurred while running the command: {e}")
            # Pass the error to the Error method
            self.Error(str(e))
