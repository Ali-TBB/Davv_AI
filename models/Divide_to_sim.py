
import json
import google.generativeai as genai
from BaseModel import BaseModel


class Divide_to_sim(BaseModel):
    def __init__(self, model, filename=None):
        super().__init__(JPath="dataset/Data_Divide_to_sm.json", filename=filename)
        self.model = model
        self.convo = None
        self.history_handler = self.Backup()
        self.convo = self.model.start_chat(history=self.history_handler.history)

    
    def Run(self, input_msg, image_path=None, voice_path=None , update=True):

        if image_path:
            upload_file = genai.upload_file(image_path, mime_type="image/png")
            self.convo.send_message([input_msg, upload_file])
        elif voice_path:
            upload_file = genai.upload_file(voice_path, mime_type="audio/wav")
            self.convo.send_message([input_msg, upload_file])
        else:
            self.convo.send_message(input_msg)
        output_msg = self.convo.last.text
        if update:
            self.update_history(input_msg, output_msg, image_path, voice_path)
        json_data = json.loads(self.split_output(output_msg))
        for step_name in json_data:
            step = json_data[step_name]
            if step["action"] == "create_file":
                self.create_file(step["file_name"], step["code"])
            if step["action"] == "run_command":
                self.save_command(step["code"])
        return json_data

    def create_file(self, file_name, code):
        try:
            # Write command content to a temporary Python script
            with open(file_name, "w") as file:
                file.write(code)
            print(f"file created {file_name}")
        except Exception as e:
            print(f"An error occurred while saving the file {file_name}: {e}")

    def open_file(self, file_name):

        pass
