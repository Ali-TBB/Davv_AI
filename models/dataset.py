from utils.collection import Collection


class Dataset(Collection):
    """
    Represents a dataset.

    Attributes:
        table (str): The name of the table in the database.
    """

    table = "datasets"

    def __init__(self, id, name, backup_id=None, created_at=None, updated_at=None):
        """
        Initialize a Dataset object.

        Args:
            id (int): The ID of the dataset.
            name (str): The name of the dataset.
            backup_id (int, optional): The ID of the backup dataset (default: None).
            created_at (datetime, optional): The creation timestamp of the dataset (default: None).
            updated_at (datetime, optional): The last update timestamp of the dataset (default: None).
        """

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
        """
        Get the name of the dataset.

        Returns:
            str: The name of the dataset.
        """

        return self.get("name")

    @name.setter
    def name(self, value):
        """
        Set the name of the dataset.

        Args:
            value (str): The new name for the dataset.
        """

        self.set("name", value)

    @property
    def backup_id(self) -> int:
        """
        Get the backup ID of the dataset.

        Returns:
            int: The backup ID of the dataset.
        """

        return self.get("backup_id")

    @backup_id.setter
    def backup_id(self, value):
        """
        Set the backup ID of the dataset.

        Args:
            value (int): The new backup ID for the dataset.
        """

        self.set("backup_id", value)

    @property
    def backup(self):
        """
        Get the backup dataset.

        Returns:
            Dataset: The backup dataset.
        """

        return Dataset.find(self.backup_id)

    from models.dataset_item import DatasetItem

    @property
    def items(self) -> list[DatasetItem]:
        """
        Get the items in the dataset.

        Returns:
            list[DatasetItem]: The items in the dataset.
        """

        from models.dataset_item import DatasetItem

        return DatasetItem.all(f"`dataset_id` = {self.id}")

    @property
    def all_items(self) -> list[DatasetItem]:
        """
        Get all items in the dataset, including items from the backup dataset.

        Returns:
            list[DatasetItem]: All items in the dataset.
        """

        return (self.backup.items if self.backup else []) + self.items

    def addItem(self, role: str, parts: list):
        """
        Add an item to the dataset.

        Args:
            role (str): The role of the item.
            parts (list): The parts of the item.

        Returns:
            DatasetItem: The created dataset item.
        """

        from models.dataset_item import DatasetItem

        return DatasetItem.create(None, self.id, role, parts)
