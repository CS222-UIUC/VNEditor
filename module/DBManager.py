"""
A general database key-value PDO
"""

import os
import sqlite3
from .Exception import *


class DBManager:
    """
    PDO for split3 database, stimulate key-value database schema
    """

    def __init__(self, db_dir):
        """
        constructor for DBManager

        @param db_dir: database directory
        """
        self.__cursor = None
        self.DB = None
        self.connect(db_dir)

    def create_table_if_not_exist(self, table_name: str):
        """
        create table via given table name, do nothing if table already exist

        @param table_name: table name
        @return:
        """
        self.__cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {table_name}
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL  ,
                            Key TEXT            NOT NULL UNIQUE ,
                            Value Text          NOT NULL)"""
        )

    def push(self, key: str, value: str, table_name: str):
        """
        push key-value into specified table

        @param key: key to push
        @param value: corresponding value
        @param table_name: table name
        @return:
        """
        try:
            self.__cursor.execute(
                'INSERT INTO {} (Key,Value) Values ("{}", "{}")'.format(
                    table_name, key, value
                )
            )
        except sqlite3.Error:
            raise DBManagerError(
                "key '{}' already exist in table '{}'".format(key, table_name)
            )

    def push_dict(self, data: dict, table_name: str):
        """
        push a dictionary into table
        @param data: data in dict format
        @param table_name: table name
        @return:
        """
        for key in data.keys():
            self.push(key, data[key], table_name)

    def update(self, key: str, value: str, table_name: str):
        """
        update value corresponding to given key in given table
        @param key: key name
        @param value: value name
        @param table_name: table name
        @return:
        """
        try:
            self.__cursor.execute(
                'UPDATE {} SET Value="{}" WHERE Key="{}"'.format(table_name, value, key)
            )
        except sqlite3.Error as e:
            raise DBManagerError(str(e))

    def remove(self, key: str, table_name: str):
        """
        remove item with given key from table given

        @param key: key name
        @param table_name: table name
        @return:
        """
        try:
            self.__cursor.execute(
                'DELETE from {} where key="{}"'.format(table_name, key)
            )
        except sqlite3.Error as e:
            raise DBManagerError(str(e))

    def drop_table(self, table_name: str):
        """
        drop the table with given table name

        @param table_name: table name
        @return:
        """
        try:
            self.__cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        except sqlite3.Error:
            raise DBManagerError("drop table {} fail".format(table_name))

    def select(self, table_name: str, is_desc: bool = False, amount: int = -1) -> dict:
        """
        select items from table given

        @param table_name: table name
        @param is_desc: is ordered descend
        @param amount: amount item to be selected, if overflow or -1, select all items
        @return: selected items
        """
        arg_LIMIT = "LIMIT " + str(amount) if amount != -1 else ""
        arg_DESC = "ORDERED BY Value DESC" if is_desc else ""
        try:
            data = self.__cursor.execute(
                "SELECT id, key, value  from {} {} {}".format(
                    table_name, arg_LIMIT, arg_DESC
                )
            )
        except Exception:
            raise DBManagerError(
                "error occur when select from table: {}".format(table_name)
            )
        out = {}
        for row in data:
            out[row[1]] = row[2]
        return out

    def commit(self):
        """
        commit database change

        @return:
        """
        try:
            self.DB.commit()
        except Exception:
            raise DBManagerError("error occur when commit database")

    def close(self):
        """
        close the database

        @return:
        """
        try:
            self.DB.close()
        except Exception:
            raise DBManagerError("error occur when close database")

    def connect(self, db_dir):
        """
        connect the database

        @param db_dir: database directory
        @return:
        """
        if not os.path.exists(db_dir):
            print("create new db: %s in: " % db_dir)
        else:
            print("connect to db: %s" % db_dir)
        self.DB = sqlite3.connect(db_dir)
        self.__cursor = self.DB.cursor()


if __name__ == "__main__":
    print("Load DBManager Class")
