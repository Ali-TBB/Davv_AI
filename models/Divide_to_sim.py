
from FileHistory import ChatHistoryHandler
import google.generativeai as genai

class Divide_to_sim():
    def __init__(self, model):
        self.model = model
    
    def Run(self, input) -> tuple:
        history_handler = ChatHistoryHandler("dataset/Divide_to_sim.json")
        convo = self.model.start_chat(history=history_handler.history)
        convo.send_message(input)
        outputme = convo.last.text
        new_chat_entry = {"role": "user", "parts": ["{}".format(input)]}
        history_handler.update_history(new_chat_entry)
        new_chat_entry = {"role": "model", "parts": ["{}".format(outputme)]}
        history_handler.update_history(new_chat_entry)
        history_handler.save_history()