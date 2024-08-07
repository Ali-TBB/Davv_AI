import os
import sqlite3
from utils.env import Env


class Database:

    __connection: sqlite3.Connection = None

    @classmethod
    def install(cls):
        sql_file_path = os.path.join(Env.base_path, "database/database.sql")

        with open(sql_file_path, "r") as sqlFile:
            print("Creating database...")
            for sql in sqlFile.read().split(";".strip()):
                cls.execute(sql)
            print("Database created successfully")

        from utils import seeder

        seeder.seed()

    @classmethod
    def execute(cls, sql, params=()) -> sqlite3.Cursor:
        try:
            cursor = cls.connection.cursor()
            cursor.execute(sql, params)
            cls.connection.commit()
            return cursor
        except Exception as e:
            print(f"Error executing SQL query '{sql}'\params: {params}", e)
            raise e

    @classmethod
    def close(cls):
        if cls.__connection:
            cls.__connection.close()
            cls.__connection = None
            print("Database connection closed")

    @classmethod
    @property
    def connection(cls) -> sqlite3.Connection:
        if cls.__connection is None:
            db_path = os.path.join(Env.base_path, "database/database.db")

            install = not os.path.exists(db_path)

            cls.__connection = sqlite3.connect(db_path)

            if install:
                cls.install()

        return cls.__connection
