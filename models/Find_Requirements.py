from BaseModel import BaseModel
from models.FileHistory import ChatHistoryHandler


class Find_Requirements(BaseModel):
    def __init__(self):
        super().__init__(JPath="dataset/chat_history.json")

    def Run(self, value):
        history_handler = ChatHistoryHandler(self.jpath)
        convo = self.model.start_chat(history=history_handler.history)
        convo.send_message(value)
        outputme = convo.last.text
        new_chat_entry = {"role": "user", "parts": ["{}".format(value)]}
        history_handler.update_history(new_chat_entry)
        new_chat_entry = {"role": "model", "parts": ["{}".format(outputme)]}
        history_handler.update_history(new_chat_entry)
        history_handler.save_history()
        if "#screenshot" in outputme:
            return "#screenshot"
        elif "#simple" in outputme:
            return "#simple"
        elif "#big" in outputme:
            return "#big"
        else:
            return -1