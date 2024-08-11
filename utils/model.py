import datetime

import utils
from utils.collection import Collection


class Model:
    """
    A utility class for performing common database operations.

    Methods:
    - all: Retrieve all records from a table.
    - findWhere: Retrieve a single record from a table based on a condition.
    - nextId: Get the next available ID for a table.
    - create: Insert a new record into a table.
    - updateWhere: Update records in a table based on a condition.
    - update: Update a specific record in a table.
    - deleteWhere: Delete records from a table based on a condition.
    - delete: Delete a specific record from a table.
    - truncate: Delete all records from a table.
    """

    @staticmethod
    def all(
        collection_cls,
        table,
        where=None,
        params=(),
        order_by="created_at",
        order_type="ASC",
        **kwargs,
    ) -> list[Collection]:
        """
        Retrieve all records from a table.

        Args:
        - collection_cls: The class representing the collection of records.
        - table: The name of the table.
        - where: The condition to filter the records (optional).
        - params: The parameters to be used in the SQL query (optional).
        - order_by: The column to order the records by (default: "created_at").
        - order_type: The order type ("ASC" or "DESC", default: "ASC").
        - kwargs: Additional keyword arguments to be passed to the collection class constructor.

        Returns:
        - A list of collection objects representing the retrieved records.
        """

        sql = f"SELECT * FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        if order_by:
            sql += f" ORDER BY `{order_by}` {order_type}"
        rows: list[Collection] = []
        for row in utils.Database.execute(sql, params).fetchall():
            rows.append(collection_cls(*row, **kwargs))
        return rows

    @staticmethod
    def findWhere(
        collection_cls, table, where: str, params=(), **kwargs
    ) -> "Collection":
        """
        Retrieve a single record from a table based on a condition.

        Args:
        - collection_cls: The class representing the collection of records.
        - table: The name of the table.
        - where: The condition to filter the record.
        - params: The parameters to be used in the SQL query (optional).
        - kwargs: Additional keyword arguments to be passed to the collection class constructor.

        Returns:
        - A collection object representing the retrieved record, or None if not found.
        """

        row = utils.Database.execute(
            f"SELECT * FROM `{table}` WHERE {where}", params
        ).fetchone()
        return collection_cls(*row, **kwargs) if row else None

    @classmethod
    def nextId(cls, table, index="id") -> int:
        """
        Get the next available ID for a table.

        Args:
        - table: The name of the table.
        - index: The name of the ID column (default: "id").

        Returns:
        - The next available ID for the table.
        """

        row = utils.Database.execute(f"SELECT MAX(`{index}`) FROM `{table}`").fetchone()
        return row[0] + 1 if row[0] else 1

    @staticmethod
    def create(table, item: utils.Collection, auto_increment=True) -> int:
        """
        Insert a new record into a table.

        Args:
        - table: The name of the table.
        - item: The collection object representing the record to be inserted.
        - auto_increment: Whether to automatically assign an ID to the record (default: True).

        Returns:
        - The ID of the inserted record.
        """

        if not item.id:
            id = Model.nextId(table) if auto_increment else item.id
            item.id = id
        if not item.created_at:
            item.created_at = datetime.datetime.now()
        if not item.updated_at:
            item.updated_at = datetime.datetime.now()

        sql = f"INSERT INTO `{table}` (`{'`, `'.join(item.data.keys())}`) VALUES ({', '.join(['?' for _ in item.data.values()])})"
        cur = utils.Database.execute(sql, list(item.data.values()))
        return cur.lastrowid

    @staticmethod
    def updateWhere(table, data: dict, where=None) -> int:
        """
        Update records in a table based on a condition.

        Args:
        - table: The name of the table.
        - data: A dictionary containing the column-value pairs to be updated.
        - where: The condition to filter the records (optional).

        Returns:
        - The number of updated records.
        """

        data["updated_at"] = datetime.datetime.now()
        sql = (
            f"UPDATE `{table}` SET {', '.join([f'`{key}` = ?' for key in data.keys()])}"
        )
        if where:
            sql += f" WHERE {where}"

        return utils.Database.execute(sql, list(data.values())).rowcount

    @staticmethod
    def update(table, item: utils.Collection, index="id") -> bool:
        """
        Update a specific record in a table.

        Args:
        - table: The name of the table.
        - item: The collection object representing the record to be updated.
        - index: The name of the ID column (default: "id").

        Returns:
        - True if the record was successfully updated, False otherwise.
        """

        return Model.updateWhere(table, item.data, f"`{index}` = {item.id}") > 0

    @staticmethod
    def deleteWhere(table, where=None, params=()) -> int:
        """
        Delete records from a table based on a condition.

        Args:
        - table: The name of the table.
        - where: The condition to filter the records (optional).
        - params: The parameters to be used in the SQL query (optional).

        Returns:
        - The number of deleted records.
        """

        sql = f"DELETE FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        return utils.Database.execute(sql, params).rowcount

    @staticmethod
    def delete(table, id, index="id") -> bool:
        """
        Delete a specific record from a table.

        Args:
        - table: The name of the table.
        - id: The ID of the record to be deleted.
        - index: The name of the ID column (default: "id").

        Returns:
        - True if the record was successfully deleted, False otherwise.
        """

        return Model.deleteWhere(table, f"`{index}` = {id}") > 0

    @staticmethod
    def truncate(table) -> int:
        """
        Delete all records from a table.

        Args:
        - table: The name of the table.

        Returns:
        - The number of deleted records.
        """

        return Model.deleteWhere(table)
