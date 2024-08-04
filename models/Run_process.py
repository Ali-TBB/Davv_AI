#!/usr/bin/python3
'''module Run_process'''
import json
from BaseModel import BaseModel, create_model
from FixError import FixError
import google.generativeai as genai

class Run_process(BaseModel):
    def __init__(self, model, filename=None):
        super().__init__("dataset/data.json", filename)
        self.model = model
        self.convo = None
        history_handler = self.Backup()
        self.convo = self.model.start_chat(history=history_handler.history)

    def Error(self, issue):
        issue = f"#error {issue}"
        Fixer = FixError(issue, model = create_model())
        Fixer.Run()
        #re run the command
        self.Run(Error_fixed=True)

    def Run(self, input_msg=None, Error_fixed=False, image_path=None, voice_path=None):

        if not Error_fixed :
            if image_path:
                upload_file = genai.upload_file(image_path, mime_type="image/png")
                self.convo.send_message([input_msg, upload_file])
            elif voice_path:
                upload_file = genai.upload_file(voice_path, mime_type="audio/wav")
                self.convo.send_message([input_msg, upload_file])
            else:
                self.convo.send_message(input_msg)
            output_msg = self.convo.last.text
            self.update_history(input_msg, output_msg, image_path, voice_path)
        json_data = json.loads(self.split_output(output_msg))
        if json_data["action"] == "execute":
            if json_data["language"] == "python":
                self.save_command(json_data["code"])
                self.Run_command()
        elif json_data["action"] == "response":
            response =  json_data["response"]
            print(response)
