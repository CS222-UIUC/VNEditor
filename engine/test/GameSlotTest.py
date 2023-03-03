import unittest
from module.ProjectManager import ProjectManagerError
from module.GameSlot import GameSlot
from module.DBManager import DBManager
from module.ConfigManager import Loader
from utils import file_utils
from module.Exception import *


class GameSlotTest(unittest.TestCase):
    CONFIG_DIR = "../service.ini"
    GAME_DB_NAME = "test.db"
    game_slot = GameSlot(db_dir=GAME_DB_NAME, config_dir=CONFIG_DIR)

    def test_reset(self):
        self.game_slot.reset()
        self.assertTrue(file_utils.check_file_valid(self.GAME_DB_NAME))

    def test_drop(self):
        self.game_slot.drop()
        with self.assertRaises(DBManagerError):
            self.game_slot.get_all_progress()

    def test_dump(self):
        self.game_slot.reset()
        self.game_slot.dump_progress(12)
        self.assertEqual(len(self.game_slot.get_all_progress()), 1)
        self.assertEqual(int(self.game_slot.get_all_progress()[0]["frame"]), 12)

    def test_multi_dump(self):
        self.game_slot.reset()

        for i in range(1000):
            self.game_slot.dump_progress(i)

        all_process = self.game_slot.get_all_progress()
        all_process_frame = [i["frame"] for i in all_process]
        expect_frame = list(range(1000))

        self.assertEqual(len(self.game_slot.get_all_progress()), 1000)

        for idx, i in enumerate(expect_frame):
            self.assertEqual(str(i), all_process_frame[idx])


if __name__ == "__main__":
    unittest.main()
