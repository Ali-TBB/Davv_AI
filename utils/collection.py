import datetime
import json


import utils


class Collection:
    """
    A class representing a collection.

    Attributes:
        table (str): The name of the table associated with the collection.
        index (str): The name of the index column.
        auto_increment (bool): Indicates whether the collection has auto-incrementing IDs.
        __data (dict): The data stored in the collection.

    Methods:
        __init__(self, data): Initializes a new instance of the Collection class.
        id(self): Gets the ID of the collection.
        id(self, value): Sets the ID of the collection.
        created_at(self): Gets the creation timestamp of the collection.
        created_at(self, value): Sets the creation timestamp of the collection.
        updated_at(self): Gets the last update timestamp of the collection.
        updated_at(self, value): Sets the last update timestamp of the collection.
        all(cls, where=None, params=(), order_by="created_at", order_type="ASC", **kwargs): Retrieves all collections from the database.
        findWhere(cls, where=None, params=(), **kwargs): Retrieves a collection based on the specified conditions.
        find(cls, id, **kwargs): Retrieves a collection by its ID.
        nextId(cls): Retrieves the next available ID for the collection.
        create(cls, *args, **kwargs): Creates a new collection.
        update(self): Updates the collection in the database.
        delete(self): Deletes the collection from the database.
        truncate(cls): Deletes all collections from the database.
        set(self, key, value): Sets the value of a specific key in the collection.
        get(self, key): Retrieves the value of a specific key from the collection.
        data(self): Retrieves a copy of the data stored in the collection.
        __str__(self): Returns a string representation of the collection.
        __dict__(self): Returns a dictionary representation of the collection.
        listen(cls, event, callback): Registers a callback function to be called when a specific event occurs.
        onEvent(cls, event, *args): Triggers the specified event and calls the registered callback functions.
        onDeleting(cls, collection, *args): Event handler called before a collection is deleted.
        onDeleted(cls, collection, *args): Event handler called after a collection is deleted.
    """

    table: str
    index = "id"
    auto_increment = True
    __data: dict


    def __init__(self, data):
        """
        Initializes an instance of MyClass.

        Args:
            data (dict): A dictionary containing the data for the instance.

        Attributes:
            __data (dict): The data for the instance.
        """

        data["created_at"] = str(data["created_at"]) if data.get("created_at") else None
        data["updated_at"] = str(data["updated_at"]) if data.get("updated_at") else None
        self.__data = data

    @property
    def id(self):
        """
        Returns the value of the 'id' attribute.

        Returns:
            The value of the 'id' attribute.
        """

        return self.get("id")

    @id.setter
    def id(self, value):
        """
        Set the ID of the object.

        Args:
            value (int): The ID value to set.

        Returns:
            None
        """

        self.set("id", value)

    @property
    def created_at(self) -> datetime.datetime:
        """
        Returns the value of the 'created_at' attribute as datetime.

        Returns:
            The value of the 'id' attribute as datetime.
        """

        return (
            datetime.datetime.fromisoformat(self.get("created_at"))
            if self.get("created_at")
            else None
        )

    @created_at.setter
    def created_at(self, value: datetime.datetime):
        """
        Set the 'created_at' attribute of the object.

        Args:
            value (datetime.datetime): The value to set as the 'created_at' attribute.

        Returns:
            None
        """

        self.set("created_at", str(value))

    @property
    def updated_at(self) -> datetime.datetime:
        """
        Returns the datetime object representing the last updated timestamp of the collection.
        If the "updated_at" key is not present in the collection, returns None.
        """

        return (
            datetime.datetime.fromisoformat(self.get("updated_at"))
            if self.get("updated_at")
            else None
        )

    @updated_at.setter
    def updated_at(self, value: datetime.datetime):
        """
        Sets the 'updated_at' attribute of the object.

        Args:
            value (datetime.datetime): The value to set as the 'updated_at' attribute.

        Returns:
            None
        """

        self.set("updated_at", str(value))

    @classmethod
    def all(
        cls, where=None, params=(), order_by="created_at", order_type="ASC", **kwargs
    ) -> list["Collection"]:
        """
        Retrieve all instances of the Collection class from the database.

        Args:
            cls (type): The Collection class.
            where (str, optional): The WHERE clause of the SQL query. Defaults to None.
            params (tuple, optional): The parameters for the SQL query. Defaults to ().
            order_by (str, optional): The column to order the results by. Defaults to "created_at".
            order_type (str, optional): The order type, either "ASC" or "DESC". Defaults to "ASC".
            **kwargs: Additional keyword arguments.

        Returns:
            list[Collection]: A list of Collection instances retrieved from the database.
        """

        return utils.Model.all(
            cls, cls.table, where, params, order_by, order_type, **kwargs
        )

    @classmethod
    def findWhere(cls, where=None, params=(), **kwargs) -> "Collection":
        """
        Find records in the collection that match the given conditions.

        Args:
            cls: The class of the collection.
            where: The WHERE clause of the SQL query.
            params: The parameters to be used in the SQL query.
            **kwargs: Additional keyword arguments.

        Returns:
            A new Collection object containing the matching records.
        """

        return utils.Model.findWhere(cls, cls.table, where, params, **kwargs)

    @classmethod
    def find(cls, id, **kwargs) -> "Collection":
        """
        Find a collection item by its ID.

        Args:
            id: The ID of the item to find.
            **kwargs: Additional keyword arguments to pass to the `findWhere` method.

        Returns:
            The found collection item.

        """

        return cls.findWhere(f"`{cls.index}` = ?", (id,), **kwargs)

    @classmethod
    def nextId(cls) -> int:
        """
        Returns the next available ID for the given table.

        Args:
            cls: The class representing the table.

        Returns:
            int: The next available ID.

        """

        return utils.Model.nextId(cls.table)

    @classmethod
    def create(cls, *args, **kwargs) -> "Collection":
        """
        Create a new instance of the Collection class.

        Args:
            cls: The Collection class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The newly created Collection instance.

        """

        collection = cls(*args, **kwargs)
        res = utils.Model.create(cls.table, collection, cls.auto_increment)
        cls.onEvent("creating", collection, res)
        return collection

    def update(self) -> bool:
        """
        Updates the current instance in the database.

        Returns:
            bool: True if the update was successful, False otherwise.
        """

        res = utils.Model.update(self.__class__.table, self)
        self.__class__.onEvent("updating", self, res)
        return res

    def delete(self) -> bool:
        """
        Deletes the current object from the database.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """

        self.__class__.onEvent("deleting", self)
        res = utils.Model.delete(self.__class__.table, self.id)
        self.__class__.onEvent("deleted", self, res)
        return res

    @classmethod
    def truncate(cls) -> int:
        """
        Truncates the table associated with the given class.

        Returns:
            int: The number of rows affected by the truncation.
        """

        return utils.Model.truncate(cls.table)

    def set(self, key, value):
        """
        Sets the value of a key in the collection.

        Args:
            key (str): The key to set the value for.
            value (Any): The value to set.

        Raises:
            Exception: If the key is "id" and it already exists in the collection.
            Exception: If the key is "created_at" and it already exists in the collection.
            Exception: If the key is "updated_at" and it already exists in the collection.
            Exception: If the key does not exist in the collection.
        """

        if key == "id" and self.get("id"):
            raise Exception("You can't update the id of a collection")
        elif key == "created_at" and self.get("created_at"):
            raise Exception("You can't update the created_at of a collection")
        elif key == "updated_at" and self.get("updated_at"):
            raise Exception("You can't update the updated_at of a collection")
        elif not key in self.__data:
            raise Exception(f"Key {key} not found in the collection")

        self.__data[key] = value

    def get(self, key) -> any:
        """
        Retrieve the value associated with the given key.

        Args:
            key: The key to retrieve the value for.

        Returns:
            The value associated with the given key, or None if the key is not found.
        """

        return self.__data.get(key)

    @property
    def data(self) -> dict:
        """
        Returns a copy of the data stored in the collection.

        Returns:
            dict: A copy of the data stored in the collection.
        """

        return self.__data.copy()

    def __str__(self) -> str:
        """
        Returns a string representation of the object.

        Returns:
            str: A string representation of the object.
        """

        data = self.data.copy()
        data["created_at"] = str(data["created_at"])
        data["updated_at"] = str(data["updated_at"])

        return f"{self.__class__.__name__}: {json.dumps(data, indent=2)}"

    def __dict__(self) -> dict:
        """
        Returns a dictionary representation of the object, excluding the 'updated_at' key.
        
        Returns:
            dict: A dictionary representation of the object.
        """

        data = self.data.copy()
        data.pop("updated_at")
        return data

    listeners = {
        "creating": [],
        "created": [],
        "updating": [],
        "updated": [],
        "deleting": [],
        "deleted": [],
    }

    @classmethod
    def listen(cls, event: str, callback: callable):
        """
        Add a callback function to the listeners for a specific event.

        Args:
            event (str): The name of the event.
            callback (callable): The callback function to be added.

        Raises:
            Exception: If the event is invalid.

        """

        if not event in cls.listeners:
            raise Exception("Invalid event")
        if not callback in cls.listeners[event]:
            cls.listeners[event].append(callback)

    @classmethod
    def onEvent(cls, event, *args):
        """
        Handle the specified event and call the corresponding callbacks.

        Args:
            cls: The class object.
            event (str): The event to handle.
            *args: Additional arguments to pass to the callbacks.

        Returns:
            None
        """

        if event == "deleted":
            cls.onDeleted(*args)
        elif event == "deleting":
            cls.onDeleting(*args)
        for callback in cls.listeners[event]:
            callback(cls, *args)

    @classmethod
    def onDeleting(cls, collection, *args):
        """
        This method is called when an item is being deleted from the collection.

        Args:
            collection: The collection from which the item is being deleted.
            *args: Additional arguments that may be passed.

        Returns:
            None
        """

        pass

    @classmethod
    def onDeleted(cls, collection, *args):
        """
        This method is called when an item is deleted from the collection.

        Args:
            collection: The collection from which the item is deleted.
            *args: Additional arguments that may be passed.

        Returns:
            None
        """

        pass
