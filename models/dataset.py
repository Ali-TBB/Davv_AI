from utils.collection import Collection


class Dataset(Collection):

    table = "datasets"

    def __init__(self, id, name, backup_id=None, created_at=None, updated_at=None):
        super().__init__(
            {
                "id": id,
                "name": name,
                "backup_id": backup_id,
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
    def backup_id(self) -> int:
        return self.get("backup_id")

    @backup_id.setter
    def backup_id(self, value):
        self.set("backup_id", value)

    @property
    def backup(self):
        return Dataset.find(self.backup_id)

    from models.dataset_item import DatasetItem

    @property
    def items(self) -> list[DatasetItem]:
        from models.dataset_item import DatasetItem

        return DatasetItem.all(f"`dataset_id` = {self.id}")

    @property
    def all_items(self) -> list[DatasetItem]:
        return (self.backup.items if self.backup else []) + self.items

    def addItem(self, role: str, parts: list):
        from models.dataset_item import DatasetItem

        return DatasetItem.create(None, self.id, role, parts)
