import os

from dotenv import load_dotenv, set_key, find_dotenv


class Env:
    """
    A utility class for managing environment variables.
    """

    @classmethod
    @property
    def base_path(cls):
        """
        Get the base path of the current file.
        """

        return "\\".join(os.path.dirname(__file__).split("\\")[0:-1])

    @staticmethod
    def init():
        """
        Initialize the environment by loading the .env file if it exists, or creating it if it doesn't.
        """

        env_path = find_dotenv()
        if not env_path:
            with open(os.path.join(Env.base_path, ".env"), "w") as f:
                pass
            env_path = find_dotenv()
        load_dotenv()

    @staticmethod
    def get(key) -> str:
        """
        Get the value of an environment variable.

        Args:
            key: The name of the environment variable.

        Returns:
            The value of the environment variable as a string.
        """

        return os.environ.get(key)

    def set(key, value):
        """
        Set the value of an environment variable.

        Args:
            key: The name of the environment variable.
            value: The value to be set.

        """

        os.environ[key] = value
        set_key(find_dotenv(), key, value)

    def unset(key):
        """
        Unset an environment variable.

        Args:
            key: The name of the environment variable to unset.
        """

        del os.environ[key]

    @classmethod
    @property
    def all(cls) -> dict:
        """
        Get all environment variables as a dictionary.

        Returns:
            A dictionary containing all environment variables.
        """

        return os.environ

    @staticmethod
    def has(key) -> bool:
        """
        Check if an environment variable exists.

        Args:
            key: The name of the environment variable to check.

        Returns:
            True if the environment variable exists, False otherwise.
        """

        return key in os.environ
