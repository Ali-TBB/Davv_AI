import datetime
import json


import utils


class Collection:
    auto_increment = True
    table: str
    __data: dict

    def __init__(self, data):
        data["created_at"] = str(data["created_at"]) if data.get("created_at") else None
        data["updated_at"] = str(data["updated_at"]) if data.get("updated_at") else None
        self.__data = data

    @property
    def id(self):
        return self.get("id")

    @id.setter
    def id(self, value):
        self.set("id", value)

    @property
    def created_at(self) -> datetime.datetime:
        return (
            datetime.datetime.fromisoformat(self.get("created_at"))
            if self.get("created_at")
            else None
        )

    @created_at.setter
    def created_at(self, value: datetime.datetime):
        self.set("created_at", str(value))

    @property
    def updated_at(self) -> datetime.datetime:
        return (
            datetime.datetime.fromisoformat(self.get("updated_at"))
            if self.get("updated_at")
            else None
        )

    @updated_at.setter
    def updated_at(self, value: datetime.datetime):
        self.set("updated_at", str(value))

    @classmethod
    def all(cls, where=None) -> list["Collection"]:
        return utils.Model.all(cls, cls.table, where)

    @classmethod
    def find(cls, id, index="id") -> "Collection":
        return utils.Model.find(cls, cls.table, id, index)

    @classmethod
    def nextId(cls) -> int:
        return utils.Model.nextId(cls.table)

    @classmethod
    def create(cls, collection) -> int:
        res = utils.Model.create(cls.table, collection, cls.auto_increment)
        cls.onEvent("creating", collection, res)
        return res

    @classmethod
    def new(cls) -> "Collection":
        raise Exception("Method new not implemented")

    def update(self) -> bool:
        res = utils.Model.update(self.__class__.table, self)
        self.__class__.onEvent("updating", self, res)
        return res

    def save(self) -> int | bool:
        if self.id:
            return self.update()
        else:
            return self.__class__.create(self)

    def delete(self) -> bool:
        self.__class__.onEvent("deleting", self)
        res = utils.Model.delete(self.__class__.table, self.id)
        self.__class__.onEvent("deleted", self, res)
        return res

    @classmethod
    def truncate(cls) -> int:
        return utils.Model.truncate(cls.table)

    def set(self, key, value):
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
        return self.__data.get(key)

    @property
    def data(self) -> dict:
        return self.__data.copy()

    def __str__(self) -> str:
        data = self.data
        data["created_at"] = str(data["created_at"])
        data["updated_at"] = str(data["updated_at"])
        return f"{self.__class__.__name__}: {json.dumps(data, indent=2)}"

    def __dict__(self) -> dict:
        return self.data

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
        if not event in cls.listeners:
            raise Exception("Invalid event")
        if not callback in cls.listeners[event]:
            cls.listeners[event].append(callback)

    @classmethod
    def onEvent(cls, event, *args):
        if event == "deleted":
            cls.onDeleted(*args)
        elif event == "deleting":
            cls.onDeleting(*args)
        for callback in cls.listeners[event]:
            callback(cls, *args)

    @classmethod
    def onDeleting(cls, collection, *args):
        pass

    @classmethod
    def onDeleted(cls, collection, *args):
        pass
