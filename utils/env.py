import os
from dotenv import load_dotenv, set_key, find_dotenv


class Env:

    @classmethod
    @property
    def base_path(cls):
        return "\\".join(os.path.dirname(__file__).split("\\")[0:-1])

    @staticmethod
    def init():
        env_path = find_dotenv()
        if not env_path:
            with open(os.path.join(Env.base_path, ".env"), "w") as f:
                pass
            env_path = find_dotenv()
        load_dotenv()

    @staticmethod
    def get(key) -> str:
        return os.environ.get(key)

    def set(key, value):
        os.environ[key] = value
        set_key(find_dotenv(), key, value)

    def unset(key):
        del os.environ[key]

    @classmethod
    @property
    def all(cls) -> dict:
        return os.environ

    @staticmethod
    def has(key) -> bool:
        return key in os.environ
