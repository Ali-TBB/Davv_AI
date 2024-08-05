from utils.collection import Collection


class Attachment(Collection):

    table = "attachments"

    def __init__(self, id, name, path, created_at=None, updated_at=None):
        super().__init__(
            {
                "id": id,
                "name": name,
                "path": path,
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
    def path(self) -> str:
        return self.get("path")

    @path.setter
    def path(self, value):
        self.set("path", value)
