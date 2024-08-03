#!/usr/bin/python3
'''module Run_process'''
import os
import time
import pyautogui
from BaseModel import BaseModel, create_model
from FileHistory import ChatHistoryHandler
from FixError import FixError
import subprocess
import google.generativeai as genai

class Run_process(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__("dataset/data.json", *args, **kwargs)
        self.convo = None
        history_handler = self.Backup()
        self.convo = self.model.start_chat(history=history_handler.history)

    def Error(self, issue, value):
        issue = f"#error {issue}"
        Fixer = FixError(issue, model = create_model)
        Fixer.Run()
        #re run the command
        self.Run(value , update=False)

    def Run(self, value, update=True, with_screenshot=False):

        if with_screenshot:
            full_path = self.take_screenshot()
            upload_file = genai.upload_file(full_path, mime_type="image/png")
            print(f"Uploaded file '{upload_file.display_name}' as: {upload_file.uri}")
            self.convo.send_message([value, upload_file])
            outputme = self.convo.last.text
            foundcode = self.Split_output(outputme)
        else:
            self.convo.send_message(value)
            outputme = self.convo.last.text
            foundcode = self.Split_output(outputme)

        if update :
            history_handler = ChatHistoryHandler(self.JPath)
            if with_screenshot:
                new_chat_entry = {"role": "user", "parts": ["{}".format(value), f"image : {full_path}"]}
            new_chat_entry = {"role": "user", "parts": ["{}".format(value)]}
            history_handler.update_history(new_chat_entry)
            new_chat_entry = {"role": "model", "parts": ["{}".format(outputme)]}
            history_handler.update_history(new_chat_entry)
            history_handler.save_history()

        if foundcode:
            print("Operation is runing ...")
            try:
                # Execute the command using subprocess
                result = subprocess.run(["python", "command.py"], capture_output=True)
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
                self.Error(str(e), value)
   
    def take_screenshot(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        t = time.strftime("%y_%m_%d_%H%M%S")
        full_path = os.path.join(current_dir, "screenshot_image/" + f"{t}.png")
        try:
            # Capture the screenshot
            screenshot = pyautogui.screenshot()
            # Save the screenshot to the specified file path
            screenshot.save(full_path)
            print("Screenshot saved successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
        return full_path

    def Backup(self):
        history_handler = ChatHistoryHandler(self.JPath)
        history_handler.Backup_history()
        i = 0
        for entry in history_handler.history:
            for part in entry["parts"]:
                if "image :" in part:
                    image_path = part.split("image : ")[-1].strip()
                    upload_file = genai.upload_file(image_path, mime_type="image/png")
                    history_handler.history[i]["parts"][1] = upload_file 
            i += 1
        return history_handler