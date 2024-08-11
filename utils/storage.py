import json
import os


from utils.env import Env


def get_storage():
    """
    Returns the storage directory.

    Returns:
    - The storage directory.
    """

    return Directory(os.path.join(Env.base_path, "run/browser/web/storage"))


class Directory:
    """
    Represents a directory in the file system.

    Attributes:
        __path (str): The path of the directory.

    Methods:
        __init__(self, path: str): Initializes a new instance of the Directory class.
        path(self) -> str: Gets the path of the directory.
        name(self) -> str: Gets the name of the directory.
        create(self): Creates the directory if it doesn't exist.
        delete(self): Deletes the directory if it exists.
        items(self) -> list: Gets a list of items (files and subdirectories) in the directory.
        file(self, file: str): Creates a File object for the specified file in the directory.
        directory(self, directory: str): Creates a Directory object for the specified subdirectory.
    """

    __path: str

    def __init__(self, path: str):
        """
        Initializes a Storage object with the given path.

        Args:
            path (str): The path to the storage directory.

        Raises:
            Exception: If the provided path is not a directory.
        """

        self.__path = path
        if os.path.exists(path) and not os.path.isdir(path):
            raise Exception(f"Path '{path}' is not a directory")

    @property
    def path(self) -> str:
        """
        Returns the path of the storage.

        If the path does not exist, it will be created before returning.

        Returns:
            str: The path of the storage.
        """

        if not os.path.exists(self.__path):
            self.create()
        return self.__path

    @property
    def name(self) -> str:
        """
        Returns the name of the file or directory.
        
        Returns:
            str: The name of the file or directory.
        """

        return os.path.basename(self.path)

    def create(self):
        """
        Creates a directory at the specified path if it doesn't already exist.
        """

        if not os.path.exists(self.__path):
            os.makedirs(self.__path)

    def delete(self):
        """
        Deletes the directory specified by the path if it exists.

        Raises:
            OSError: If the directory does not exist or cannot be deleted.
        """

        if os.path.exists(self.__path):
            os.rmdir(self.__path)

    def items(self) -> list:
        """
        Returns a list of items in the storage path.

        Each item in the list can be either a file or a directory.

        Returns:
            list: A list of items in the storage path.
        """

        return [
            self.file(item) if os.path.isfile(item) else self.directory(item)
            for item in os.listdir(self.path)
        ]

    def file(self, file: str):
        """
        Returns a File object associated with the specified file.

        Args:
            file (str): The name of the file.

        Returns:
            File: The File object associated with the specified file.
        """

        return File(self, file)

    def directory(self, directory: str):
        """
        Creates a new Directory object within the current storage path.

        Args:
            directory (str): The name of the directory to create.

        Returns:
            Directory: A new Directory object representing the created directory.
        """

        return Directory(os.path.join(self.path, directory))


class File:
    """
    Represents a file in a directory.

    Attributes:
        directory (Directory): The directory where the file is located.
        filename (str): The name of the file.
    """

    directory: "Directory"

    def __init__(self, directory: "Directory", filename: str):
        """
        Initializes a new instance of the File class.

        Args:
            directory (Directory): The directory where the file is located.
            filename (str): The name of the file.

        Raises:
            Exception: If the path is not a file.
        """

        self.directory = directory
        self.filename = filename
        if os.path.exists(self.path) and not os.path.isfile(self.path):
            raise Exception(f"Path '{self.path}' is not a file")

    @property
    def path(self) -> str:
        """
        Gets the full path of the file.

        Returns:
            str: The full path of the file.
        """

        return os.path.join(self.directory.path, self.filename)

    @property
    def name(self) -> str:
        """
        Gets the name of the file.

        Returns:
            str: The name of the file.
        """

        return os.path.basename(self.path)

    @property
    def content(self) -> str | list | dict:
        """
        Gets the content of the file.

        Returns:
            str | list | dict: The content of the file. If the content is a valid JSON, it is returned as a parsed object.
        """

        if os.path.exists(self.path):
            with open(self.path, "r") as file:
                content = file.read()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content

    def set(self, content: str | list | dict | bytes):
        """
        Sets the content of the file.

        Args:
            content (str | list | dict | bytes): The content to be set in the file.
        """

        if isinstance(content, bytes):
            with open(self.path, "wb") as file:
                file.write(content)
        else:
            if isinstance(content, (list, dict)):
                content = json.dumps(content, indent=4)

            with open(self.path, "w") as file:
                file.write(content)
