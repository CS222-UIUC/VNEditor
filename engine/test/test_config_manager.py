import sys

sys.path.append("..")

from unittest import TestCase
from module.config_manager import ConfigLoader
from utils.exception import ConfigLoaderError


class TestConfigLoader(TestCase):
    CONFIG_DIR = "../service.ini"
    config = ConfigLoader(CONFIG_DIR)

    def test_game_memory(self):
        game_memory_config = self.config.game_save()
        self.assertEqual(game_memory_config["slot_name"], "slot")

    def test_engine(self):
        game_memory_config = self.config.engine()
        self.assertEqual(game_memory_config["loader"], "pickle_loader")

    def test_log_file(self):
        game_log_config = self.config.log_file()
        self.assertEqual(game_log_config["default_suffix"], "log")

    def test_resources(self):
        game_memory_config = self.config.resources()
        self.assertEqual(game_memory_config["background_dir"], "resources/background")

    def test_project(self):
        game_project_config = self.config.project()
        self.assertEqual(game_project_config["projects_base"], "./projects")

    def test_version(self):
        game_version_config = self.config.version()
        self.assertEqual(game_version_config["name"], "VNEditor Service")

    def test_cors(self):
        game_cors_config = self.config.cors()
        self.assertEqual(game_cors_config["origins"], "*")

    def test_get_all_section(self):
        game_cors_config = self.config.get_all_section()
        self.assertNotEqual(len(game_cors_config), 0)

    def test_log_error(self):
        with self.assertRaises(ConfigLoaderError):
            ConfigLoader("not_exist.txt")
