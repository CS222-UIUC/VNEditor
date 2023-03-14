import sys

sys.path.append("..")

import os
from unittest import TestCase
from utils import file_utils


class TestFileUtils(TestCase):
    def test_check_file_valid(self):
        self.assertFalse(file_utils.check_file_valid("aaaa"))

    def test_check_folder_valid(self):
        self.assertFalse(file_utils.check_folder_valid("aaaa"))

    def test_get_files_in_folder(self):
        self.assertEqual(len(file_utils.get_files_in_folder("aaa")), 0)
        self.assertNotEqual(len(file_utils.get_files_in_folder("./")), 0)
        self.assertEqual(len(file_utils.get_files_in_folder("./", suffix=".py")), 0)

    def test_get_folders_in_folder(self):
        self.assertEqual(len(file_utils.get_folders_in_folder("aaa")), 0)
        self.assertNotEqual(len(file_utils.get_folders_in_folder("../")), 0)

    def test_get_all_in_folder(self):
        self.assertEqual(len(file_utils.get_all_in_folder("aaa")), 0)

    def test_get_folder_dir(self):
        self.assertIsNotNone(len(file_utils.get_folder_dir("aaa")))

    def test_get_ext(self):
        self.assertIsNotNone(len(file_utils.get_ext("aaa.txt")))

    def test_rename_file(self):
        self.assertFalse(file_utils.rename_file("aaaa", "bbbb"))
        fo = open("test_file", "w")
        fo.close()

        self.assertTrue(file_utils.rename_file("test_file", "test_file.txt"))
        file_utils.delete_file("test_file.txt")

    def test_delete_file(self):
        self.assertFalse(file_utils.delete_file("aaaaa"))

    def test_delete_folder(self):
        os.mkdir("aaa")
        self.assertTrue(file_utils.delete_folder("aaa"))
        self.assertFalse(file_utils.delete_folder("aaaaaa"))
