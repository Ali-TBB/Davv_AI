import os

from utils.collection import Collection
from utils.database import Database
from utils.env import Env
from utils.model import Model


def list_dir(path, deep=True, only_files=False):
    if not os.path.exists(path):
        raise Exception("Invalid path, the path doesn't exists")
    elif not os.path.isdir(path):
        raise Exception("Invalid path, this path is not a directory")

    paths = []
    for item in os.listdir(path):
        itemPath = os.path.join(path, item)

        if os.path.isdir(item):
            if not only_files:
                paths.append(itemPath)
            if deep:
                paths.append(*list_dir(itemPath))
        else:
            paths.append(itemPath)

    return paths
