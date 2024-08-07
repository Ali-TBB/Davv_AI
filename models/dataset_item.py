import json

from utils.collection import Collection


class DatasetItem(Collection):

    table = "dataset_items"

    def __init__(self, id, dataset_id, role, parts, created_at=None, updated_at=None):
        super().__init__(
            {
                "id": id,
                "dataset_id": dataset_id,
                "role": role,
                "parts": json.dumps(parts) if type(parts) != str else parts,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def dataset_id(self) -> int:
        return self.get("dataset_id")

    @dataset_id.setter
    def dataset_id(self, value):
        self.set("dataset_id", value)

    @property
    def dataset(self):
        return DatasetItem.find(self.dataset_id)

    @property
    def role(self) -> str:
        return self.get("role")

    @role.setter
    def role(self, value):
        self.set("role", value)

    @property
    def parts(self) -> list:
        return json.loads(self.get("parts"))

    @parts.setter
    def parts(self, value: list):
        self.set("parts", json.dumps(value))
