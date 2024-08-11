import json
import os
import platform

import pyautogui

from models.attachment import Attachment
from models.conversation import Conversation
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from models.message import Message
from utils.collection import Collection
from utils.env import Env
from utils import list_dir

tables: dict[str, Collection] = {
    "datasets": Dataset,
    "dataset_items": DatasetItem,
    "conversation": Conversation,
    "messages": Message,
    "attachments": Attachment,
}


variables = {
    "OS_SYSTEM": platform.system(),
    "SIZE": pyautogui.size(),
}


def seed():
    """
    Seed the database with data from JSON seed files.

    This function truncates all tables in the database, then reads JSON seed files
    from the specified directory and populates the tables with the data. The JSON
    files should contain a "table" key specifying the table name and an "items" key
    containing a list of items to be inserted into the table.

    Raises:
        Exception: If the JSON seed file is invalid or if the specified table does not exist.
    """

    [table.truncate() for table in tables.values()]

    path = os.path.join(Env.base_path, "database/seeders")
    pathFiles = list_dir(path, only_files=True)

    for filePath in pathFiles:
        if filePath.endswith(".json"):
            content = open(filePath, "r").read()
            for variable, value in variables.items():
                content = content.replace(f"<-{variable}->", str(value))
            seeder = json.loads(content)
            if not ("table" in seeder or "items" in seeder):
                raise Exception("Invalid seeder, missing table or items key")
            elif not seeder["table"] in tables:
                raise Exception(
                    f"Invalid table, table '{seeder['table']}' doesn't exists"
                )
            for item in seeder["items"]:
                collector = tables[seeder["table"]]
                collector.create(**item)
