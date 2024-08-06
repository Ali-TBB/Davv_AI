import json
import os


from utils.env import Env


def get_storage():
    return Directory(os.path.join(Env.base_path, "storage"))


class Directory:

    path: str

    def __init__(self, path: str):
        self.path = path
        if os.path.exists(self.path) and not os.path.isdir(self.path):
            raise Exception(f"Path '{self.path}' is not a directory")

    def create(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def delete(self):
        if os.path.exists(self.path):
            os.rmdir(self.path)

    def items(self) -> list:
        return [
            self.file(item) if os.path.isfile(item) else self.directory(item)
            for item in os.listdir(self.path)
        ]

    def file(self, file: str):
        self.create()
        return File(self, file)

    def directory(self, directory: str):
        self.create()
        return Directory(os.path.join(self.path, directory))


class File:

    directory: "Directory"

    def __init__(self, directory: "Directory", filename: str):
        self.directory = directory
        self.filename = filename
        if os.path.exists(self.path) and not os.path.isfile(self.path):
            raise Exception(f"Path '{self.path}' is not a file")

    @property
    def path(self) -> str:
        return os.path.join(self.directory.path, self.filename)

    @property
    def content(self) -> str | list | dict:
        if os.path.exists(self.path):
            with open(self.filename, "r") as file:
                content = file.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content

    def set(self, content: str | list | dict | bytes):
        if isinstance(content, bytes):
            with open(self.filename, "wb") as file:
                file.write(content)
        else:
            if isinstance(content, (list, dict)):
                content = json.dumps(content, indent=4)

            with open(self.filename, "w") as file:
                file.write(content)
