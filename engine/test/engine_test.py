"""
test case for engine
"""

import sys

sys.path.append("..")

import unittest
from engine.engine import Engine
from module.project_manager import ProjectManager

CONFIG_DIR = "../service.ini"
PROJECT_DIR = "./test_project"


class EngineTest(unittest.TestCase):
    def test_initialize(self):
        try:
            project = ProjectManager()
            abs_project_addr = project.init_project(
                base_dir=PROJECT_DIR, config_dir=CONFIG_DIR
            )
            engine = Engine(project_dir=abs_project_addr, config_dir=CONFIG_DIR)
            self.project = project
            self.engine = engine
        except Exception as e:
            self.fail("fail due to: %s" % str(e))
