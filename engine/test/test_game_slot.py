import sys

sys.path.append("..")

from unittest import TestCase
from module.gamesave_module import GameSave, get_cur_time, parse_data
from utils import file_utils
from utils.exception import *


class TestGameSlot(TestCase):
    CONFIG_DIR = "../service.ini"
    PROJECT_DIR = "./"
    game_slot = GameSave(project_dir=PROJECT_DIR, config_dir=CONFIG_DIR)

    def test_reset(self):
        self.game_slot.reset()
        self.assertTrue(file_utils.check_folder_valid(self.PROJECT_DIR))

    def test_drop(self):
        self.game_slot.drop()
        with self.assertRaises(DBManagerError):
            self.game_slot.get_all_progress()

    def test_get_slot_name(self):
        self.assertNotEqual(self.game_slot.get_slot_name(), "")

    def test_dump_progress(self):
        self.game_slot.reset()
        self.game_slot.dump_progress(12)
        self.assertEqual(len(self.game_slot.get_all_progress()), 1)
        self.assertEqual(int(self.game_slot.get_all_progress()[0]["frame"]), 12)

    def test_remove_progress(self):
        self.game_slot.remove_progress("12")

    def test_get_all_progress(self):
        self.assertNotEqual(len(self.game_slot.get_all_progress()), 0)

    def test_get_current_time(self):
        self.assertIsNotNone(get_cur_time())

    def test_parse_data(self):
        self.assertEqual(parse_data({"1": 1}), str({"1": 1}))

    def test_zprint(self):
        self.game_slot.print()
        self.game_slot.dump_progress(12)
        self.game_slot.print()
        self.game_slot.print(limit=1)
        self.game_slot.print(limit=20)
        self.game_slot.close()
