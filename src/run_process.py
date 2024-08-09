"""module run_process"""

from models.attachment import Attachment
from src.base_model import BaseModel
from src.data_types.run_process import RunProcessDataType


class RunProcess(BaseModel):
    """
    Represents a process runner.

    Args:
        BaseModel: The base model class.

    Attributes:
        convo: The conversation object.
    """

    data_type = RunProcessDataType

    backup_name = "run_process"

    def handle_output(self, input_msg, output_msg, attachments: list[Attachment] = []):
        self.update_history(input_msg, output_msg, attachments)

        json_data = self.parse_output(output_msg)
        if "action" in json_data:
            if json_data["action"] == "execute":
                if json_data["language"] == "python":
                    return json_data["response"], self.run_command(
                        "command.py", json_data["code"]
                    )
                elif json_data["language"] == "shell":
                    return json_data["response"], self.run_command(
                        "command.sh", json_data["code"]
                    )
                else:
                    return f"Invalid language {json_data['language']}.", None
        if "response" in json_data:
            return json_data["response"], None
        else:
            return f"Invalid command.", None
