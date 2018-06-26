import unittest
from root_dir import ROOT_DIR
from pathlib import Path

from util.path import compare_filenames_in_path, path_points_to_directory, path_points_to_file, string_after_last_slash
from util.path import create_directory

PATH_TO_FOLDER = ROOT_DIR + '/tests/test_data'
PATH_TO_FILE = ROOT_DIR + '/tests/test_data/string_test_should'

FILENAME_1 = 'abc/dfg/SAME'
FILENAME_2 = 'qwe/rtt/SAME'
FILENAME_3 = 'poi/uzt/rew'

FILENAME_WITHOUT_SLASH = "qwertz"

DIRECTORY_TO_CREATE_PATH = ROOT_DIR + "/tests/testDirectory"


class PathTest(unittest.TestCase):

    def test_compare_equal_filenames_in_path(self):
        res = compare_filenames_in_path(FILENAME_1, FILENAME_2)
        self.assertTrue(res)

    def test_compare_different_filenames_in_path(self):
        res = compare_filenames_in_path(FILENAME_1, FILENAME_3)
        self.assertFalse(res)

    def test_path_points_to_directory(self):
        res = path_points_to_directory(PATH_TO_FOLDER)
        self.assertTrue(res)

    def test_path_does_not_point_to_directory(self):
        res = path_points_to_directory(PATH_TO_FILE)
        self.assertFalse(res)

    def test_path_points_to_file(self):
        res = path_points_to_file(PATH_TO_FILE)
        self.assertTrue(res)

    def test_path_does_not_point_to_file(self):
        res = path_points_to_file(PATH_TO_FOLDER)
        self.assertFalse(res)

    def test_cut_with_two_slashes(self):
        res = string_after_last_slash(FILENAME_3)
        self.assertEqual("rew", res)

    def test_cut_without_slash(self):
        res = string_after_last_slash(FILENAME_WITHOUT_SLASH)
        self.assertEqual(FILENAME_WITHOUT_SLASH, res)

    def test_create_directory(self):
        create_directory(DIRECTORY_TO_CREATE_PATH)
        res = path_points_to_directory(DIRECTORY_TO_CREATE_PATH)
        helper_path = Path(DIRECTORY_TO_CREATE_PATH)
        helper_path.rmdir()
        self.assertTrue(res)