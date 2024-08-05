import os
import json

from utils import list_dir
from utils.env import Env
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from models.conversation import Conversation
from models.message import Message
from models.attachment import Attachment

tables = {
    "datasets": Dataset,
    "dataset_items": DatasetItem,
    "conversation": Conversation,
    "messages": Message,
    "attachments": Attachment,
}


def seed():
    Dataset.truncate()
    DatasetItem.truncate()

    path = os.path.join(Env.base_path, "database/seeders")
    pathFiles = list_dir(path, only_files=True)

    for filePath in pathFiles:
        if filePath.endswith(".json"):
            print("Seeding ", filePath)
            seeder = json.loads(open(filePath, "r").read())
            if not ("table" in seeder or "items" in seeder):
                raise Exception("Invalid seeder, missing table or items key")
            elif not seeder["table"] in tables:
                raise Exception(f"Invalid table, table '{seeder["table"]}' doesn't exists")
            for item in seeder["items"]:
                print("Seeding item: ", item)
                collector = tables[seeder["table"]]
                collection = tables[seeder["table"]](**item)
                print(collection)
                collector.create(collection)
