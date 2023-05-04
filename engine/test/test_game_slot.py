import sys

sys.path.append("..")

from unittest import TestCase
from module.gamesave_module import GameSave, get_cur_time, parse_data
from utils import file_utils
from utils.exception import *


class TestGameSlot(TestCase):
    """
    A test case class for testing the GameSave class.
    """

    CONFIG_DIR = "../service.ini"
    PROJECT_DIR = "./"
    game_slot = GameSave(project_dir=PROJECT_DIR, config_dir=CONFIG_DIR)

    def test_reset(self):
        """
        Test case for the reset method of GameSave.
        It resets the game slot and asserts that the project directory is valid.
        """
        self.game_slot.reset()
        self.assertTrue(file_utils.check_folder_valid(self.PROJECT_DIR))

    def test_drop(self):
        """
        Test case for the drop method of GameSave.
        It drops the game slot and asserts that all progress is removed.
        """
        self.game_slot.drop()
        with self.assertRaises(DBManagerError):
            self.game_slot.get_all_progress()

    def test_get_slot_name(self):
        """
        Test case for the get_slot_name method of GameSave.
        It asserts that the slot name is not an empty string.
        """
        self.assertNotEqual(self.game_slot.get_slot_name(), "")

    def test_dump_progress(self):
        """
        Test case for the dump_progress method of GameSave.
        It resets the game slot, dumps progress, and asserts that the progress is added.
        """
        self.game_slot.reset()
        self.game_slot.dump_progress(12)
        self.assertEqual(len(self.game_slot.get_all_progress()), 1)
        self.assertEqual(int(self.game_slot.get_all_progress()[0]["frame"]), 12)

    def test_remove_progress(self):
        """
        Test case for the remove_progress method of GameSave.
        It removes progress with the specified frame ID.
        """
        self.game_slot.remove_progress("12")

    def test_get_all_progress(self):
        """
        Test case for the get_all_progress method of GameSave.
        It asserts that there is progress stored in the game slot.
        """
        self.assertNotEqual(len(self.game_slot.get_all_progress()), 0)

    def test_get_current_time(self):
        """
        Test case for the get_cur_time function.
        It asserts that the current time is not None.
        """
        self.assertIsNotNone(get_cur_time())

    def test_parse_data(self):
        """
        Test case for the parse_data function.
        It parses a data dictionary and asserts that the parsed result is a string.
        """
        self.assertEqual(parse_data({"1": 1}), str({"1": 1}))

    def test_zprint(self):
        """
        Test case for the print method of GameSave.
        It tests various print scenarios including no limit, a specified limit,
        and closing the game slot after printing.
        """
        self.game_slot.print()
        self.game_slot.dump_progress(12)
        self.game_slot.print()
        self.game_slot.print(limit=1)
        self.game_slot.print(limit=20)
        self.game_slot.close()
