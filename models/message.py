import json

from utils.collection import Collection
from models.attachment import Attachment


class Message(Collection):

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
        self.validate("role", role)

        super().__init__(
            {
                "id": id,
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "attachments_ids": (
                    json.dumps(attachments_ids)
                    if type(attachments_ids) == list
                    else attachments_ids
                ),
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def conversation_id(self) -> int:
        return self.get("conversation_id")

    @conversation_id.setter
    def conversation_id(self, value):
        self.set("conversation_id", value)

    def conversation(self):
        from models.conversation import Conversation

        return Conversation.find(self.conversation_id)

    @property
    def role(self) -> str:
        return self.get("role")

    def validate(self, target, value):
        if target == "role" and value not in ["user", "model"]:
            raise Exception("Invalid role")

    @role.setter
    def role(self, value):
        self.validate("role", value)
        self.set("role", value)

    @property
    def content(self) -> str:
        return self.get("content")

    @content.setter
    def content(self, value):
        self.set("content", value)

    @property
    def attachments_ids(self) -> str:
        return json.loads(self.get("attachments_ids"))

    @attachments_ids.setter
    def attachments_ids(self, value: list):
        self.set("attachments_ids", json.dumps(value))

    def attachments(self) -> list[Attachment]:
        return Attachment.all(f"`id` IN ({', '.join(self.attachments_ids)})")
