import os
import json
import platform

import pyautogui

from utils import list_dir
from utils.collection import Collection
from utils.env import Env
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from models.conversation import Conversation
from models.message import Message
from models.attachment import Attachment

tables: dict[str, Collection] = {
    "datasets": Dataset,
    "dataset_items": DatasetItem,
    "conversation": Conversation,
    "messages": Message,
    "attachments": Attachment,
}


variables = {
    "OS_SYSTEM": platform.system(),
    "SIZE": pyautogui.size,
}


def seed():
    [table.truncate() for table in tables.values()]

    path = os.path.join(Env.base_path, "database/seeders")
    pathFiles = list_dir(path, only_files=True)

    for filePath in pathFiles:
        if filePath.endswith(".json"):
            content = open(filePath, "r").read()
            for variable, value in variables.items():
                content = content.replace(f"<-${variable}->", value)
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
