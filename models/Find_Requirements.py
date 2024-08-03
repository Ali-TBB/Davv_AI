from BaseModel import BaseModel
from FileHistory import ChatHistoryHandler


class Find_Requirements(BaseModel):
    def __init__(self, model):
        super().__init__(JPath="dataset/data_find_req.json")
        self.model = model

    def Run(self, value) -> tuple:
        history_handler = ChatHistoryHandler(self.JPath)
        convo = self.model.start_chat(history=history_handler.history)
        convo.send_message(value)
        outputme = convo.last.text
        new_chat_entry = {"role": "user", "parts": ["{}".format(value)]}
        history_handler.update_history(new_chat_entry)
        new_chat_entry = {"role": "model", "parts": ["{}".format(outputme)]}
        history_handler.update_history(new_chat_entry)
        history_handler.save_history()
        if "#screenshot" in outputme:
            return "#screenshot", value
        elif "#simple" in outputme:
            return "#simple", value
        elif "#big" in outputme:
            return "#big", value
        else:
            return -1, value