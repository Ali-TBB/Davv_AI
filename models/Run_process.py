#!/usr/bin/python3
'''module Run_process'''
from BaseModel import BaseModel, create_model
from FileHistory import ChatHistoryHandler
from FixError import FixError
import subprocess
import google.generativeai as genai

class Run_process(BaseModel):
    def __init__(self, model, filename=None):
        super().__init__("dataset/data.json", filename)
        self.model = model
        self.convo = None
        history_handler = self.Backup()
        self.convo = self.model.start_chat(history=history_handler.history)

    def Error(self, issue, value):
        issue = f"#error {issue}"
        Fixer = FixError(issue, model = create_model())
        Fixer.Run()
        #re run the command
        self.Run(value , update=False)

    def Run(self, value, update=True, image_path=None, voice_path=None):

        if image_path:
            upload_file = genai.upload_file(image_path, mime_type="image/png")
            self.convo.send_message([value, upload_file])
        elif voice_path:
            upload_file = genai.upload_file(voice_path, mime_type="audio/wav")
            self.convo.send_message([value, upload_file])
        else:
            self.convo.send_message(value)
        output_msg = self.convo.last.text
        found_code = self.Split_output(output_msg)

        if update :
            history_handler = ChatHistoryHandler(self.JPath)
            if image_path:
                new_chat_entry = {"role": "user", "parts": ["{}".format(value), f"image : {image_path}"]}
            elif voice_path:
                new_chat_entry = {"role": "user", "parts": ["{}".format(value), f"voice : {voice_path}"]}
            new_chat_entry = {"role": "user", "parts": ["{}".format(value)]}
            history_handler.update_history(new_chat_entry)
            new_chat_entry = {"role": "model", "parts": ["{}".format(output_msg)]}
            history_handler.update_history(new_chat_entry)
            history_handler.save_history()

        if found_code:
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