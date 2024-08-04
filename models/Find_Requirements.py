import json
from BaseModel import BaseModel
from FileHistory import ChatHistoryHandler


class Find_Requirements(BaseModel):
    def __init__(self, model):
        super().__init__(JPath="dataset/data_find_req.json")
        self.model = model

    def Run(self, input_msg) -> tuple:
        history_handler = ChatHistoryHandler(self.JPath)
        convo = self.model.start_chat(history=history_handler.history)
        convo.send_message(input_msg)
        output_msg = convo.last.text
        new_chat_entry = {"role": "user", "parts": ["{}".format(input_msg)]}
        history_handler.update_history(new_chat_entry)
        new_chat_entry = {"role": "model", "parts": ["{}".format(output_msg)]}
        history_handler.update_history(new_chat_entry)
        history_handler.save_history()
        json_data = json.loads(self.split_output(output_msg))
        if json_data["action"] == "#response":
            response = json_data["response"]
            return "#response", response
        elif json_data["action"] == "#simple":
            return "#simple", input_msg
        elif json_data["action"] == "#screenshot":
            return "#screenshot", input_msg
        elif json_data["action"] == "#big":
            return "#big", input_msg
