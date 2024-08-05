from utils.collection import Collection


class Dataset(Collection):

    table = "datasets"

    def __init__(self, id, name, type, created_at=None, updated_at=None):
        super().__init__(
            {
                "id": id,
                "name": name,
                "type": type,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def type(self) -> str:
        return self.get("type")

    @type.setter
    def type(self, value):
        self.set("type", value)

    @property
    def name(self) -> str:
        return self.get("name")

    @name.setter
    def name(self, value):
        self.set("name", value)

    from models.dataset_item import DatasetItem

    @property
    def items(self) -> list[DatasetItem]:
        from models.dataset_item import DatasetItem

        return DatasetItem.all(f"`dataset_id` = {self.id}")

    def addItem(self, role: str, parts: list):
        from models.dataset_item import DatasetItem

        return DatasetItem.create(
            DatasetItem(
                dataset_id=self.id,
                role=role,
                parts=parts,
            )
        )
