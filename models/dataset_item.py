import json

from utils.collection import Collection


class DatasetItem(Collection):
    """
    Represents an item in a dataset.

    Attributes:
        table (str): The name of the table in the database.
    """

    table = "dataset_items"

    def __init__(self, id, dataset_id, role, parts, created_at=None, updated_at=None):
        """
        Initializes a new instance of the DatasetItem class.

        Args:
            id (int): The ID of the dataset item.
            dataset_id (int): The ID of the dataset that the item belongs to.
            role (str): The role of the item in the dataset.
            parts (list): The parts of the item.
            created_at (datetime, optional): The creation timestamp of the item. Defaults to None.
            updated_at (datetime, optional): The last update timestamp of the item. Defaults to None.
        """

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
        """
        Gets the ID of the dataset that the item belongs to.

        Returns:
            int: The dataset ID.
        """

        return self.get("dataset_id")

    @dataset_id.setter
    def dataset_id(self, value):
        """
        Sets the ID of the dataset that the item belongs to.

        Args:
            value (int): The dataset ID.
        """

        self.set("dataset_id", value)

    @property
    def dataset(self):
        """
        Gets the dataset that the item belongs to.

        Returns:
            DatasetItem: The dataset item.
        """

        return DatasetItem.find(self.dataset_id)

    @property
    def role(self) -> str:
        """
        Gets the role of the item in the dataset.

        Returns:
            str: The role.
        """

        return self.get("role")

    @role.setter
    def role(self, value):
        """
        Sets the role of the item in the dataset.

        Args:
            value (str): The role.
        """

        self.set("role", value)

    @property
    def parts(self) -> list:
        """
        Gets the parts of the item.

        Returns:
            list: The parts.
        """

        return json.loads(self.get("parts"))

    @parts.setter
    def parts(self, value: list):
        """
        Sets the parts of the item.

        Args:
            value (list): The parts.
        """

        self.set("parts", json.dumps(value))
