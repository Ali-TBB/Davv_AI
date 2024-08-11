import os

from utils.collection import Collection
from utils.database import Database
from utils.env import Env
from utils.model import Model


def list_dir(path, deep=True, only_files=False):
    """
    Recursively lists all files and directories in the given path.

    Args:
        path (str): The path to the directory.
        deep (bool, optional): If True, lists files and directories recursively. Defaults to True.
        only_files (bool, optional): If True, only lists files and excludes directories. Defaults to False.

    Returns:
        list: A list of paths to files and directories.
    """

    if not os.path.exists(path):
        raise Exception("Invalid path, the path doesn't exist")
    elif not os.path.isdir(path):
        raise Exception("Invalid path, this path is not a directory")

    paths = []
    for item in os.listdir(path):
        itemPath = os.path.join(path, item)

        if os.path.isdir(item):
            if not only_files:
                paths.append(itemPath)
            if deep:
                paths += list_dir(itemPath)
        else:
            paths.append(itemPath)

    return paths
