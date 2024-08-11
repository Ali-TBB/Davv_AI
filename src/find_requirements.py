from models.attachment import Attachment
from src.base_model import BaseModel
from src.data_types.find_requirements import FindRequirementsDataType


class FindRequirements(BaseModel):
    """
    Class representing the FindRequirements functionality.

    Attributes:
        backup_name (str): The name of the backup.
        data_type (FindRequirementsDataType): The data type for FindRequirements.
    """

    backup_name = "find_requirement"
    data_type = FindRequirementsDataType

    def handle_output(
        self, input_msg: str, output_msg: str, attachments: list[Attachment] = []
    ):
        """
        Handles the output of the FindRequirements functionality.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            attachments (list[Attachment], optional): The list of attachments. Defaults to [].

        Returns:
            tuple: A tuple containing the action and the input message.
        """

        self.update_history(input_msg, output_msg, attachments)
        json_data = self.parse_output(output_msg)
        if "action" in json_data:
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
        else:
            print(json_data)
            return "response", (
                json_data["response"]
                if "response" in json_data
                else "Sorry, I didn't understand that."
            )
