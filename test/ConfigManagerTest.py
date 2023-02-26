import unittest
from module.ProjectManager import ProjectManagerError
from module.GameSlot import GameSlot
from module.DBManager import DBManager
from module.ConfigManager import Loader
from utils import file_utils
from module.Exception import *


class ConfigManagerTest(unittest.TestCase):
    CONFIG_DIR = '../router/service.ini'
    config = Loader(CONFIG_DIR)

    def test_load_config_game_memory(self):
        game_memory_config = self.config.game_memory()
        self.assertEqual(game_memory_config['default_slot_name'], 'slot')

    def test_load_config_engine(self):
        game_memory_config = self.config.engine()
        self.assertEqual(game_memory_config['engine'], 'engine/YuiEngine.py')

    def test_load_config_resources(self):
        game_memory_config = self.config.resources()
        self.assertEqual(game_memory_config['background_dir'], 'resources/background')

    def test_load_config_registerService(self):
        game_memory_config = self.config.register_service()
        self.assertEqual(game_memory_config['game_slot_service'], 'api/GameMemoryService.py')


if __name__ == '__main__':
    unittest.main()
