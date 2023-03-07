"""
test case for DB manager
"""
import unittest
from module.game_slot import GameSlot
from module.db_manager import DBManager
from module.config_manager import ConfigLoader
from utils import file_utils
from module.exception import *


class DBManagerTest(unittest.TestCase):
    GAME_DB_NAME = "test.db"
    db = DBManager(db_dir=GAME_DB_NAME)

    def test_create_table(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.push("key", "value", test_table_name)
        select = self.db.select(test_table_name)
        self.assertEqual(select["key"], "value")

    def test_drop_table(self):
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.commit()
        with self.assertRaises(DBManagerError):
            self.db.select(test_table_name)

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


if __name__ == "__main__":
    unittest.main()
