import sys

sys.path.append("..")

from unittest import TestCase
from module.config_module import ConfigLoader
from utils.exception import ConfigLoaderError


class TestConfigLoader(TestCase):
    """
    A test case class for testing the ConfigLoader class.
    """

    CONFIG_DIR = "../service.ini"
    config = ConfigLoader(CONFIG_DIR)

    def test_game_memory(self):
        """
        Test case for the game_save method of ConfigLoader.
        It asserts that the 'slot_name' value in the game_memory configuration is equal to 'slot'.
        """
        game_memory_config = self.config.game_save()
        self.assertEqual(game_memory_config["slot_name"], "slot")

    def test_engine(self):
        """
        Test case for the engine method of ConfigLoader.
        It asserts that the 'loader' value in the engine configuration is equal to 'pickle_loader'.
        """
        game_memory_config = self.config.engine()
        self.assertEqual(game_memory_config["loader"], "pickle_loader")

    def test_log_file(self):
        """
        Test case for the log_file method of ConfigLoader.
        It asserts that the 'default_suffix' value in the log_file configuration is equal to 'log'.
        """
        game_log_config = self.config.log_file()
        self.assertEqual(game_log_config["default_suffix"], "log")

    def test_resources(self):
        """
        Test case for the resources method of ConfigLoader.
        It asserts that the 'background_dir' value in the resources configuration is equal to 'resources/background'.
        """
        game_memory_config = self.config.resources()
        self.assertEqual(game_memory_config["background_dir"], "resources/background")

    def test_project(self):
        """
        Test case for the project method of ConfigLoader.
        It asserts that the 'projects_base' value in the project configuration is equal to './projects'.
        """
        game_project_config = self.config.project()
        self.assertEqual(game_project_config["projects_base"], "./projects")

    def test_version(self):
        """
        Test case for the version method of ConfigLoader.
        It asserts that the 'name' value in the version configuration is equal to 'VNEditor Service'.
        """
        game_version_config = self.config.version()
        self.assertEqual(game_version_config["name"], "VNEditor Service")

    def test_cors(self):
        """
        Test case for the cors method of ConfigLoader.
        It asserts that the 'origins' value in the cors configuration is equal to '*'.
        """
        game_cors_config = self.config.cors()
        self.assertEqual(game_cors_config["origins"], "*")

    def test_get_all_section(self):
        """
        Test case for the get_all_section method of ConfigLoader.
        It asserts that the returned value is not an empty dictionary.
        """
        game_cors_config = self.config.get_all_section()
        self.assertNotEqual(len(game_cors_config), 0)

    def test_log_error(self):
        """
        Test case for the ConfigLoader constructor with an invalid file path.
        It asserts that a ConfigLoaderError exception is raised.
        """
        with self.assertRaises(ConfigLoaderError):
            ConfigLoader("not_exist.txt")
