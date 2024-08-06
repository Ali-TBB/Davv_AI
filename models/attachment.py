from utils.collection import Collection


class Attachment(Collection):

    table = "attachments"

    def __init__(self, id, mime_type, path, created_at=None, updated_at=None):
        super().__init__(
            {
                "id": id,
                "mime_type": mime_type,
                "path": path,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def mime_type(self) -> str:
        return self.get("mime_type")

    @mime_type.setter
    def mime_type(self, value):
        self.set("mime_type", value)

    @property
    def path(self) -> str:
        return self.get("path")

    @path.setter
    def path(self, value):
        self.set("path", value)
