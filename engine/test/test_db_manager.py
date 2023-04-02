import sys

sys.path.append("..")
from unittest import TestCase

from module.db_manager import DBManager
from utils.exception import DBManagerError


class TestDBManager(TestCase):
    GAME_DB_NAME = "test.db"
    db = DBManager(db_dir=GAME_DB_NAME)

    def test_create_table_if_not_exist(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.push("key", "value", test_table_name)
        select = self.db.select(test_table_name)
        self.assertEqual(select["key"], "value")

    def test_push(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.create_table_if_not_exist(test_table_name)
        self.db.commit()
        self.db.push("a", "b", test_table_name)

    def test_push_dict(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.create_table_if_not_exist(test_table_name)
        self.db.commit()
        data = {}
        for i in range(100):
            data[str(i)] = "value" + str(i)
        self.db.push_dict(data, test_table_name)
        select = self.db.select(test_table_name)
        self.assertDictEqual(select, data)

    def test_update(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.create_table_if_not_exist(test_table_name)
        self.db.commit()
        self.db.push("key", "value", test_table_name)
        self.db.update("key", "value2", test_table_name)
        select = self.db.select(test_table_name)
        self.assertEqual(select["key"], "value2")

    def test_remove(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.create_table_if_not_exist(test_table_name)
        self.db.commit()
        self.db.push("key", "value", test_table_name)
        self.db.remove("key", test_table_name)

    def test_zexception(self):
        with self.assertRaises(DBManagerError):
            self.db.push("a", "a", "aaaa")
        with self.assertRaises(DBManagerError):
            self.db.update("a", "x", "aaaa")
        with self.assertRaises(DBManagerError):
            self.db.remove("a", "aaaa")
        with self.assertRaises(DBManagerError):
            self.db.select("aaaa")
        with self.assertRaises(DBManagerError):
            self.db.close()
            self.db.commit()
