import os
import sqlite3
from utils.env import Env


class Database:
    """
    A class representing a database connection and operations.

    Attributes:
        __connection (sqlite3.Connection): The connection object to the SQLite database.

    Methods:
        install(): Installs the database by executing the SQL statements from a file and performs seeding.
        execute(sql, params=()): Executes the given SQL query with optional parameters and returns the cursor.
        close(): Closes the database connection.
        connection(): Returns the database connection object.

    """

    __connection: sqlite3.Connection = None

    @classmethod
    def install(cls):
        """
        Installs the database by executing SQL statements from a file and then seeds the database.
        """

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
        """
        Executes the given SQL query with optional parameters and returns a cursor.

        Args:
            sql (str): The SQL query to execute.
            params (tuple, optional): The parameters to be passed to the query. Defaults to ().

        Returns:
            sqlite3.Cursor: The cursor object.

        Raises:
            Exception: If there is an error executing the SQL query.
        """

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
        """
        Closes the database connection if it is open.

        Args:
            cls: The class object.

        Returns:
            None
        """

        if cls.__connection:
            cls.__connection.close()
            cls.__connection = None
            print("Database connection closed")

    @classmethod
    @property
    def connection(cls) -> sqlite3.Connection:
        """
        Returns a connection to the SQLite database.

        If the connection is not already established, it creates a new connection
        to the database located at 'database/database.db' relative to the base path.

        If the database file does not exist, it installs the necessary tables by calling
        the 'install' method.

        Returns:
            sqlite3.Connection: A connection to the SQLite database.
        """

        if cls.__connection is None:
            db_path = os.path.join(Env.base_path, "database/database.db")

            install = not os.path.exists(db_path)

            cls.__connection = sqlite3.connect(db_path)

            if install:
                cls.install()

        return cls.__connection
