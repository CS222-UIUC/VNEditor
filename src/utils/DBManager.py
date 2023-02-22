import os
import sqlite3
from src.utils import MsgColor


class Service:
    def __init__(self, db_dir):
        self._cursor = None
        self.DB = None
        self.connect(db_dir)

    def create_table_if_not_exist(self, table_name: str):
        self._cursor.execute('''CREATE TABLE IF NOT EXISTS {}
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL  ,
                            Key TEXT            NOT NULL UNIQUE ,
                            Value Text          NOT NULL)'''.format(table_name))

    def push(self, key: str, value: str, table_name: str):
        try:
            self._cursor.execute("INSERT INTO {} (Key,Value) Values (\"{}\", \"{}\")".format(table_name, key, value))
        except sqlite3.Error:
            raise KeyError("key '{}' already exist in table '{}'".format(key, table_name))

    def push_dict(self, data: dict, table_name: str):
        for key in data.keys():
            self.push(key, data[key], table_name)

    def update(self, key: str, value: str, table_name: str):
        self._cursor.execute("UPDATE {} SET Value=\"{}\" WHERE Key=\"{}\"".format(table_name, value, key))

    def remove(self, key: str, table_name: str):
        self._cursor.execute("DELETE from {} where key=\"{}\"".format(table_name, key))

    def drop_table(self, table_name: str):
        self._cursor.execute("DROP TABLE IF EXISTS {}".format(table_name))
        print(MsgColor.MsgColor.OK, "(-) drop table: %s" % table_name, MsgColor.MsgColor.END)

    def select(self, table_name: str, is_desc: bool = False, amount: int = -1) -> dict:
        arg_LIMIT = "LIMIT " + str(amount) if amount != -1 else ""
        arg_DESC = "ORDERED BY Value DESC" if is_desc else ""
        data = self._cursor.execute("SELECT id, key, value  from {} {} {}".format(table_name, arg_LIMIT, arg_DESC))
        out = {}
        for row in data:
            out[row[1]] = row[2]
        return out

    def commit(self):
        self.DB.commit()

    def close(self):
        self.DB.close()

    def connect(self, db_dir):
        if not os.path.exists(db_dir):
            print("(+) create new db: %s in: " % db_dir, db_dir)
        self.DB = sqlite3.connect(db_dir)
        print(MsgColor.MsgColor.OK, "(v) find db: %s, connected" % db_dir, MsgColor.MsgColor.END)
        self._cursor = self.DB.cursor()
