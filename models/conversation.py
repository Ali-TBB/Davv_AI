from utils.collection import Collection
from models.dataset import Dataset
from models.message import Message


class Conversation(Collection):
    """
    Represents a conversation in the system.

    Attributes:
        table (str): The name of the database table for conversations.

    Args:
        id (int): The ID of the conversation.
        name (str): The name of the conversation.
        dataset_id (int): The ID of the dataset associated with the conversation.
        created_at (Optional[datetime]): The creation timestamp of the conversation.
        updated_at (Optional[datetime]): The last update timestamp of the conversation.
    """

    table = "conversations"

    def __init__(
        self, id: int, name: str, dataset_id: int, created_at=None, updated_at=None
    ):
        """
        Initializes a Conversation object.

        Args:
            id (int): The ID of the conversation.
            name (str): The name of the conversation.
            dataset_id (int): The ID of the dataset associated with the conversation.
            created_at (Optional): The creation timestamp of the conversation. Defaults to None.
            updated_at (Optional): The last update timestamp of the conversation. Defaults to None.
        """

        super().__init__(
            {
                "id": id,
                "name": name,
                "dataset_id": dataset_id,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def name(self) -> str:
        """
        Get the name of the conversation.

        Returns:
            str: The name of the conversation.
        """

        return self.get("name")

    @name.setter
    def name(self, value):
        """
        Set the name of the conversation.

        Args:
            value (str): The new name of the conversation.
        """

        self.set("name", value)

    @property
    def dataset_id(self) -> int:
        """
        Get the ID of the dataset associated with the conversation.

        Returns:
            int: The ID of the dataset.
        """

        return self.get("dataset_id")

    @dataset_id.setter
    def dataset_id(self, value: int):
        """
        Set the ID of the dataset associated with the conversation.

        Args:
            value (int): The new ID of the dataset.
        """

        self.set("dataset_id", value)

    @property
    def dataset(self) -> Dataset:
        """
        Get the dataset associated with the conversation.

        Returns:
            Dataset: The dataset associated with the conversation.
        """

        return Dataset.find(self.dataset_id)

    def messages(self) -> list[Message]:
        """
        Get all messages in the conversation.

        Returns:
            list[Message]: A list of messages in the conversation.
        """

        return Message.all(f"`conversation_id` = {self.id}")

    def send_message(
        self, role: str, content: str, attachments_ids: list = []
    ) -> Message:
        """
        Send a message in the conversation.

        Args:
            role (str): The role of the sender.
            content (str): The content of the message.
            attachments_ids (list, optional): A list of attachment IDs. Defaults to [].

        Returns:
            Message: The created message.
        """

        return Message.create(None, self.id, role, content, attachments_ids)

    @classmethod
    def onDeleting(cls, collection: "Conversation"):
        """
        Event handler called when a conversation is being deleted.

        Args:
            collection (Conversation): The conversation being deleted.
        """

        collection.dataset.delete()

        for message in collection.messages():
            message.delete()
