#!/usr/bin/python3
import os
import google.generativeai as genai
from FileHistory import ChatHistoryHandler

genai.configure(api_key="AIzaSyCudvWsPkoKlcP2YUH4t3oup2K3dnyMob8")

generation_config = {
    "temperature": 1,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = ChatHistoryHandler("safety_setting.json").history

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)


class BaseModel():
    def __init__(self, JPath, value, filename):
        self.model = model
        self.value = value
        self.JPath = JPath
        self.filename = filename

    def save_command(self, command_content):
        try:
            # Write command content to a temporary Python script
            with open(self.filename, "w") as file:
                file.write(command_content)
            print(f"Command saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving the command: {e}")

    def Split_output(self, input_str):
        code_start_index = input_str.find("#code")
        if code_start_index != -1:
            start_index = input_str.find("'''", code_start_index)
            end_index = input_str.find("'''", start_index + 3)
            if start_index != -1 and end_index != -1:
                code = input_str[start_index + 3:end_index]
                code = code.strip()
                if code:
                    self.save_command(code)
                else:
                    print("No code to save.")

    def Start(self):
        history_handler = ChatHistoryHandler(self.JPath)
        convo = self.model.start_chat(history=history_handler.history)
        convo.send_message(self.value)
        outputme = convo.last.text
        self.Split_output(outputme)
