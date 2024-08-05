import json

from src.base_model import BaseModel
from src.file_history import ChatHistoryHandler


class FindRequirements(BaseModel):
    """
    A class that represents the FindRequirements model.

    Attributes:
        JPath (str): The path to the JSON file containing the dataset.

    Methods:
        Run(input_msg) -> tuple: Runs the model with the given input message and returns the output message and action.

    """

    def __init__(self):
        super().__init__(JPath="dataset/data_find_req.json")

    def Run(self, input_msg) -> tuple:
        """
        Runs the model with the given input message and returns the output message and action.

        Args:
            input_msg (str): The input message to be processed by the model.

        Returns:
            tuple: A tuple containing the action and the output message.

        """
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
