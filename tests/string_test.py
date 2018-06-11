import unittest
from root_dir import ROOT_DIR

from util.string import to_string_with_escape_sequences

TEST_DATA_INPUT = ROOT_DIR + '/tests/test_data/string_test'
TEST_DATA_SHOULD = ROOT_DIR + '/tests/test_data/string_test_should'


class StringTest(unittest.TestCase):

    def test_escape(self):
        with open(TEST_DATA_INPUT) as fh:
            input = fh.read()
        with open(TEST_DATA_SHOULD) as fh:
            should = fh.read()
        escaped = to_string_with_escape_sequences(input)
        self.assertEqual(should, escaped)
