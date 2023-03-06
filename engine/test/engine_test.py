"""
test case for engine
"""
import unittest
from engine import yui_engine
from module import project_manager
from utils import file_utils

CONFIG_DIR = "../service.ini"
PROJECT_DIR = "./test_project"


class EngineTest(unittest.TestCase):
    def test_initialize(self):
        try:
            project = project_manager.ProjectManager(
                base_dir=PROJECT_DIR, config_dir=CONFIG_DIR
            )
            engine = yui_engine.Engine(project_dir=PROJECT_DIR, config_dir=CONFIG_DIR)
            self.project = project
            self.engine = engine
        except Exception as e:
            self.fail("fail due to: %s" % str(e))
