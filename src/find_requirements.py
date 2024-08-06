from models.attachment import Attachment
from models.dataset import Dataset
from src.base_model import BaseModel
from src.data_types.find_requirements import FindRequirementsDataType


class FindRequirements(BaseModel):
    """
    A class that represents the FindRequirements model.


    Methods:
        Run(input_msg) -> tuple: Runs the model with the given input message and returns the output message and action.

    """

    backup_name = "find_requirement"
    data_type = FindRequirementsDataType

    def handle_output(self, input_msg, output_msg, attachments: list[Attachment] = []):
        self.update_history(input_msg, output_msg, attachments)
        json_data = self.parse_output(output_msg)
        if json_data["action"] == "simple":
            return "simple", input_msg
        elif json_data["action"] == "screenshot":
            return "screenshot", input_msg
        elif json_data["action"] == "big":
            return "big", input_msg
        else:
            return "response", (
                json_data["response"]
                if "response" in json_data
                else "Sorry, I didn't understand that."
            )
