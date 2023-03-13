"""
test case for config manager
"""

import sys

sys.path.append("..")

import unittest
from module.config_manager import ConfigLoader


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
        self.assertEqual(game_memory_config["engine"], "engine/engine.py")

    def test_load_config_resources(self):
        game_memory_config = self.config.resources()
        self.assertEqual(game_memory_config["background_dir"], "resources/background")

    def test_load(self):
        game_cors_config = self.config.cors()
        self.assertEqual(game_cors_config["origins"], "*")


if __name__ == "__main__":
    unittest.main()
