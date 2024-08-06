import json

from utils.collection import Collection
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from models.message import Message


class Conversation(Collection):

    table = "conversations"

    def __init__(
        self, id: int, name: str, dataset_id: int, created_at=None, updated_at=None
    ):
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
        return self.get("name")

    @name.setter
    def name(self, value):
        self.set("name", value)

    @property
    def dataset_id(self) -> int:
        return self.get("dataset_id")

    @dataset_id.setter
    def dataset_id(self, value: int):
        self.set("dataset_id", value)

    @property
    def dataset(self) -> Dataset:
        return Dataset.find(self.dataset_id)

    def messages(self) -> list[Message]:
        return Message.all(f"`conversation_id` = {self.id}")

    def sendMessage(
        self, role: str, content: str, attachments_ids: list = []
    ) -> Message:
        return Message.create(None, self.id, role, content, attachments_ids)

    @classmethod
    def onDeleting(cls, collection):
        print("Deleting conversation", collection)
        for dataset in collection.datasets().values():
            dataset.delete()

        for message in collection.messages():
            message.delete()
