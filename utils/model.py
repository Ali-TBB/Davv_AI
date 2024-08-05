import datetime

import utils
from utils.collection import Collection


class Model:

    @staticmethod
    def all(collection_cls, table, where=None) -> list[Collection]:
        sql = f"SELECT * FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        rows: list[Collection] = []
        for row in utils.Database.execute(sql).fetchall():
            rows.append(collection_cls(*row))
        return rows

    @staticmethod
    def find(collection_cls, table, id, index="id") -> "Collection":
        row = utils.Database.execute(
            f"SELECT * FROM `{table}` WHERE `{index}` = {id}"
        ).fetchone()
        return collection_cls(*row) if row else None

    @classmethod
    def nextId(cls, table) -> int:
        row = utils.Database.execute(f"SELECT MAX(`id`) FROM `{table}`").fetchone()
        return row[0] + 1 if row[0] else 1

    @staticmethod
    def create(table, item: utils.Collection, auto_increment=True) -> int:
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
        data["updated_at"] = datetime.datetime.now()
        sql = (
            f"UPDATE `{table}` SET {', '.join([f'`{key}` = ?' for key in data.keys()])}"
        )
        if where:
            sql += f" WHERE {where}"

        return utils.Database.execute(sql, list(data.values())).rowcount

    @staticmethod
    def update(table, item: utils.Collection, index="id") -> bool:
        return Model.updateWhere(table, item.data, f"`{index}` = {item.id}") > 0

    @staticmethod
    def deleteWhere(table, where=None) -> int:
        sql = f"DELETE FROM `{table}`"
        if where:
            sql += f" WHERE {where}"
        return utils.Database.execute(sql).rowcount

    @staticmethod
    def delete(table, id, index="id") -> bool:
        return Model.deleteWhere(table, f"`{index}` = {id}") > 0

    @staticmethod
    def truncate(table) -> int:
        return Model.deleteWhere(table)
