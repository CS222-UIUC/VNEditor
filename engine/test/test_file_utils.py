import sys

sys.path.append("..")

import os
from unittest import TestCase
from utils import file_utils


class TestFileUtils(TestCase):
    """
    A test case class for testing the functions in file_utils module.
    """

    def test_check_file_valid(self):
        """
        Test case for check_file_valid function.
        It checks the validity of a non-existing file and asserts False.
        """
        self.assertFalse(file_utils.check_file_valid("aaaa"))

    def test_check_folder_valid(self):
        """
        Test case for check_folder_valid function.
        It checks the validity of a non-existing folder and asserts False.
        """
        self.assertFalse(file_utils.check_folder_valid("aaaa"))

    def test_get_files_in_folder(self):
        """
        Test case for get_files_in_folder function.
        It checks the number of files in a non-existing folder and asserts 0.
        It also checks the number of files in the current directory and asserts not equal to 0.
        It checks the number of files in the current directory with a specific suffix and asserts 0.
        """
        self.assertEqual(len(file_utils.get_files_in_folder("aaa")), 0)
        self.assertNotEqual(len(file_utils.get_files_in_folder("./")), 0)
        self.assertEqual(len(file_utils.get_files_in_folder("./", suffix=".py")), 0)

    def test_get_folders_in_folder(self):
        """
        Test case for get_folders_in_folder function.
        It checks the number of folders in a non-existing folder and asserts 0.
        It also checks the number of folders in the parent directory and asserts not equal to 0.
        """
        self.assertEqual(len(file_utils.get_folders_in_folder("aaa")), 0)
        self.assertNotEqual(len(file_utils.get_folders_in_folder("../")), 0)

    def test_get_all_in_folder(self):
        """
        Test case for get_all_in_folder function.
        It checks the number of files and folders in a non-existing folder and asserts 0.
        """
        self.assertEqual(len(file_utils.get_all_in_folder("aaa")), 0)

    def test_get_folder_dir(self):
        """
        Test case for get_folder_dir function.
        It checks the directory of a non-existing folder and asserts not None.
        """
        self.assertIsNotNone(len(file_utils.get_folder_dir("aaa")))

    def test_get_ext(self):
        """
        Test case for get_ext function.
        It checks the extension of a file and asserts not None.
        """
        self.assertIsNotNone(len(file_utils.get_ext("aaa.txt")))

    def test_rename_file(self):
        """
        Test case for rename_file function.
        It checks the renaming of a non-existing file and asserts False.
        It creates a temporary file, renames it with a different extension,
        and asserts True. Finally, it deletes the temporary file.
        """
        self.assertFalse(file_utils.rename_file("aaaa", "bbbb"))
        fo = open("test_file", "w")
        fo.close()

        self.assertTrue(file_utils.rename_file("test_file", "test_file.txt"))
        file_utils.delete_file("test_file.txt")

    def test_delete_file(self):
        """
        Test case for delete_file function.
        It checks the deletion of a non-existing file and asserts False.
        """
        self.assertFalse(file_utils.delete_file("aaaaa"))

    def test_delete_folder(self):
        """
        Test case for delete_folder function.
        It creates a temporary folder, deletes it, and asserts True.
        It also checks the deletion of a non-existing folder and asserts False.
        """
        os.mkdir("aaa")
        self.assertTrue(file_utils.delete_folder("aaa"))
        self.assertFalse(file_utils.delete_folder("aaaaaa"))
