import sys

sys.path.append("..")
from unittest import TestCase

from utils.db_utils import DBManager
from utils.exception import DBManagerError


class TestDBManager(TestCase):
    """
    A test case class for testing the DBManager class.
    """

    GAME_DB_NAME = "test.db"
    db = DBManager(db_dir=GAME_DB_NAME)

    def test_create_table_if_not_exist(self):
        """
        Test case for the create_table_if_not_exist method of DBManager.
        It creates a test table, pushes a key-value pair, and verifies the select result.
        """
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.push("key", "value", test_table_name)
        select = self.db.select(test_table_name)
        self.assertEqual(select["key"], "value")

    def test_push(self):
        """
        Test case for the push method of DBManager.
        It creates a test table, drops it, recreates it, and pushes a key-value pair.
        """
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.create_table_if_not_exist(test_table_name)
        self.db.commit()
        self.db.push("a", "b", test_table_name)

    def test_push_dict(self):
        """
        Test case for the push_dict method of DBManager.
        It creates a test table, drops it, recreates it, and pushes a dictionary of key-value pairs.
        It then verifies the select result.
        """
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
        """
        Test case for the update method of DBManager.
        It creates a test table, drops it, recreates it, pushes a key-value pair,
        updates the value, and verifies the select result.
        """
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
        """
        Test case for the remove method of DBManager.
        It creates a test table, drops it, recreates it, pushes a key-value pair,
        removes the key, and verifies the select result.
        """
        test_table_name = "test_table"
        self.db.create_table_if_not_exist(test_table_name)
        self.db.drop_table(test_table_name)
        self.db.create_table_if_not_exist(test_table_name)
        self.db.commit()
        self.db.push("key", "value", test_table_name)
        self.db.remove("key", test_table_name)

    def test_zexception(self):
        """
        Test case for handling exceptions in DBManager methods.
        It verifies that the appropriate DBManagerError exceptions are raised for invalid operations.
        """
        with self.assertRaises(DBManagerError):
            # Attempt to push to a non-existing table
            self.db.push("a", "a", "aaaa")

        with self.assertRaises(DBManagerError):
            # Attempt to update a key in a non-existing table
            self.db.update("a", "x", "aaaa")

        with self.assertRaises(DBManagerError):
            # Attempt to remove a key from a non-existing table
            self.db.remove("a", "aaaa")

        with self.assertRaises(DBManagerError):
            # Attempt to select from a non-existing table
            self.db.select("aaaa")

        with self.assertRaises(DBManagerError):
            # Attempt to close or commit the DBManager without proper initialization
            self.db.close()
            self.db.commit()