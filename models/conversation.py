import json

from utils.collection import Collection
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from models.message import Message


class Conversation(Collection):

    table = "conversations"

    def __init__(
        self, id: int, name: str, datasets_ids: list, created_at=None, updated_at=None
    ):
        super().__init__(
            {
                "id": id,
                "name": name,
                "datasets_ids": (
                    json.dumps(datasets_ids)
                    if type(datasets_ids) == list
                    else datasets_ids
                ),
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def name(self) -> str:
        return self.get("name")

    @name.setter
    def name(self, value):
        self.set("name", value)

    @property
    def datasets_ids(self) -> list:
        return json.loads(self.get("datasets_ids"))

    @datasets_ids.setter
    def datasets_ids(self, value: list):
        self.set("datasets_ids", json.dumps(value))

    def datasets(self) -> dict:
        return {
            dataset_id: Dataset.find(dataset_id) for dataset_id in self.datasets_ids
        }

    def messages(self) -> list[Message]:
        return Message.all(f"`conversation_id` = {self.id}")

    def sendMessage(
        self, role: str, content: str, attachments_ids: list = []
    ) -> Message:
        message = Message(None, self.id, role, content, attachments_ids)
        message.save()
        return message

    @classmethod
    def new(cls, name) -> "Conversation":
        conversation = Conversation(None, name, [])
        Conversation.create(conversation)
        return conversation

    @classmethod
    def onDeleting(cls, collection):
        print("Deleting conversation", collection)
        for dataset in collection.datasets().values():
            dataset.delete()

        for message in collection.messages():
            message.delete()
