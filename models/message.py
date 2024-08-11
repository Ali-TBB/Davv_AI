import json

from utils.collection import Collection
from models.attachment import Attachment


class Message(Collection):
    """
    Represents a message in a conversation.

    Attributes:
        table (str): The name of the database table for messages.
    """

    table = "messages"

    def __init__(
        self,
        id,
        conversation_id,
        role,
        content,
        attachments_ids,
        created_at=None,
        updated_at=None,
    ):
        """
        Initializes a new instance of the Message class.

        Args:
            id (int): The ID of the message.
            conversation_id (int): The ID of the conversation the message belongs to.
            role (str): The role of the sender of the message.
            content (str): The content of the message.
            attachments_ids (str): The IDs of the attachments associated with the message.
            created_at (datetime, optional): The timestamp when the message was created.
            updated_at (datetime, optional): The timestamp when the message was last updated.
        """

        self.validate("role", role)

        super().__init__(
            {
                "id": id,
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "attachments_ids": (
                    json.dumps(attachments_ids)
                    if type(attachments_ids) != str
                    else attachments_ids
                ),
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def conversation_id(self) -> int:
        """
        Gets the ID of the conversation the message belongs to.

        Returns:
            int: The conversation ID.
        """

        return self.get("conversation_id")

    @conversation_id.setter
    def conversation_id(self, value):
        """
        Sets the ID of the conversation the message belongs to.

        Args:
            value (int): The conversation ID.
        """

        self.set("conversation_id", value)

    def conversation(self):
        """
        Retrieves the conversation object associated with the message.

        Returns:
            Conversation: The conversation object.
        """

        from models.conversation import Conversation

        return Conversation.find(self.conversation_id)

    @property
    def role(self) -> str:
        """
        Gets the role of the sender of the message.

        Returns:
            str: The role.
        """

        return self.get("role")

    def validate(self, target, value):
        """
        Validates the value of a specific attribute.

        Args:
            target (str): The name of the attribute to validate.
            value: The value to validate.

        Raises:
            Exception: If the value is invalid.
        """

        if target == "role" and value not in ["user", "model"]:
            raise Exception("Invalid role")

    @role.setter
    def role(self, value):
        """
        Sets the role of the sender of the message.

        Args:
            value (str): The role.
        """

        self.validate("role", value)
        self.set("role", value)

    @property
    def content(self) -> str:
        """
        Gets the content of the message.

        Returns:
            str: The content.
        """

        return self.get("content")

    @content.setter
    def content(self, value):
        """
        Sets the content of the message.

        Args:
            value (str): The content.
        """

        self.set("content", value)

    @property
    def attachments_ids(self) -> str:
        """
        Gets the IDs of the attachments associated with the message.

        Returns:
            str: The attachments IDs.
        """

        return json.loads(self.get("attachments_ids"))

    @attachments_ids.setter
    def attachments_ids(self, value: list):
        """
        Sets the IDs of the attachments associated with the message.

        Args:
            value (list): The attachments IDs.
        """

        self.set("attachments_ids", json.dumps(value))

    def attachments(self) -> list[Attachment]:
        """
        Retrieves the attachments associated with the message.

        Returns:
            list[Attachment]: The attachments.
        """

        return Attachment.all(
            f"`id` IN ({', '.join([str(id) for id in self.attachments_ids])})"
        )

    def add_attachment(self, attachment: Attachment):
        """
        Adds an attachment to the message.

        Args:
            attachment (Attachment): The attachment to add.
        """

        self.attachments_ids.append(attachment.id)
        self.update()

    def __dict__(self) -> dict:
        """
        Converts the message object to a dictionary.

        Returns:
            dict: The message object as a dictionary.
        """

        return {
            **super().__dict__(),
            "attachments": [attachment.__dict__() for attachment in self.attachments()],
        }
