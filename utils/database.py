import os
import sqlite3
from utils.env import Env


class Database:

    __connection: sqlite3 = None

    @classmethod
    def install(cls):
        sql_file_path = os.path.join(Env.base_path, "assets", "database.sql")

        with open(sql_file_path, "r") as sqlFile:
            print("Creating database...")
            for sql in sqlFile.read().split(";".strip()):
                cls.execute(sql)
            print("Database created successfully")

    @classmethod
    def execute(cls, sql, params=()) -> sqlite3.Cursor:
        cursor = cls.connection.cursor()
        cursor.execute(sql, params)
        cls.connection.commit()
        return cursor

    @classmethod
    def close(cls):
        if cls.__connection:
            cls.__connection.close()
            cls.__connection = None
            print("Database connection closed")

    @classmethod
    @property
    def connection(cls) -> sqlite3:
        if cls.__connection is None:
            cls.__connection = sqlite3.connect(
                os.path.join(Env.base_path, "database/database.db")
            )
        return cls.__connection
