import sys

sys.path.append("..")

import unittest
import os
import tempfile
from kernel.engine_io import pickle_loader, pickle_dumper


class TestPickleIO(unittest.TestCase):
    """
    A test case class for testing the pickle_loader and pickle_dumper functions.
    """

    def setUp(self):
        """
        Set up the test data and create a temporary file for testing.
        """
        self.test_data = [{"name": "item1", "value": 1}, {"name": "item2", "value": 2}]
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)

    def tearDown(self):
        """
        Clean up by deleting the temporary file.
        """
        os.unlink(self.temp_file.name)

    def test_pickle_loader_and_dumper(self):
        """
        Test case for pickle_loader and pickle_dumper functions.
        It tests successful save and load operations, and also checks for proper handling of invalid file paths.
        """
        # Test successful save and load
        pickle_dumper(self.test_data, self.temp_file.name)
        loaded_data = pickle_loader(self.temp_file.name)
        self.temp_file.close()
        self.assertEqual(
            self.test_data, loaded_data, "Loaded data should be equal to the saved data"
        )

        # Test invalid file paths
        with self.assertRaises(FileNotFoundError):
            # Attempt to load from an invalid file path
            pickle_loader("invalid/file/path")
        with self.assertRaises(FileNotFoundError):
            # Attempt to save to an invalid file path
            pickle_dumper(self.test_data, "invalid/file/path")


if __name__ == "__main__":
    unittest.main()
