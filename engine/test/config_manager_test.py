"""
test case for config manager
"""
import unittest
from module.gameslot import GameSlot
from module.db_manager import DBManager
from module.config_manager import ConfigLoader
from utils import file_utils
from module.exception import *


class ConfigManagerTest(unittest.TestCase):
    CONFIG_DIR = "../service.ini"
    config = ConfigLoader(CONFIG_DIR)

    def test_load_config_game_memory(self):
        """
        test case for load the game memory
        @return:
        """
        game_memory_config = self.config.game_memory()
        self.assertEqual(game_memory_config["default_slot_name"], "slot")

    def test_load_config_engine(self):
        """
        test case for load the config
        @return:
        """
        game_memory_config = self.config.engine()
        self.assertEqual(game_memory_config["engine"], "engine/yui_engine.py")

    def test_load_config_resources(self):
        game_memory_config = self.config.resources()
        self.assertEqual(game_memory_config["background_dir"], "resources/background")

    def test_load_config_registerService(self):
        game_memory_config = self.config.register_service()
        self.assertEqual(
            game_memory_config["game_slot_service"], "api/GameMemoryService.py"
        )


if __name__ == "__main__":
    unittest.main()
