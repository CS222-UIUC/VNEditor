import sys

sys.path.append("..")

import unittest
import os
import tempfile
from kernel.engine_io import pickle_loader, pickle_dumper


class TestPickleIO(unittest.TestCase):
    def setUp(self):
        self.test_data = [{"name": "item1", "value": 1}, {"name": "item2", "value": 2}]
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_pickle_loader_and_dumper(self):
        # Test successful save and load
        pickle_dumper(self.test_data, self.temp_file.name)
        loaded_data = pickle_loader(self.temp_file.name)
        self.temp_file.close()
        self.assertEqual(
            self.test_data, loaded_data, "Loaded data should be equal to the saved data"
        )

        # Test invalid file paths
        with self.assertRaises(FileNotFoundError):
            pickle_loader("invalid/file/path")
        with self.assertRaises(FileNotFoundError):
            pickle_dumper(self.test_data, "invalid/file/path")


if __name__ == "__main__":
    unittest.main()
